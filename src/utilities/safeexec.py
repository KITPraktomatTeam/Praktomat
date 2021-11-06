# -*- coding: utf-8 -*-

import os
from os.path import *
import time
import subprocess
import signal
import subprocess
import resource

from django.conf import settings

def execute_arglist(args, working_directory, environment_variables={}, timeout=None, maxmem=None, fileseeklimit=None, extradirs=[], unsafe=False, error_to_output=True, filenumberlimit=128):
    """ Wrapper to execute Commands with the praktomat testuser. Excpects Command as list of arguments, the first being the execeutable to run. """
    assert isinstance(args, list)


    command = args[:]

    environment = os.environ
    environment.update(environment_variables)
    if fileseeklimit is not None:
        fileseeklimitbytes = fileseeklimit * 1024

    sudo_prefix = ["sudo", "-E", "-u", "tester"]

    if unsafe:
        command = []
    elif settings.USEPRAKTOMATTESTER:
        command = sudo_prefix
    elif settings.USESAFEDOCKER:
        command = ["sudo", "safe-docker"]
        # for safe-docker, we cannot kill it ourselves, due to sudo, so
        # rely on the timeout provided by safe-docker
        if timeout is not None:
            command += ["--timeout", "%d" % timeout]
            # give the time out mechanism below some extra time
            timeout += 5
        if maxmem is not None:
            command += ["--memory", "%sm" % maxmem]
        for d in extradirs:
            command += ["--dir", d]
        command += ["--"]
        # ensure ulimit
        if fileseeklimit:
            # Doesn’t work yet: http://stackoverflow.com/questions/25789425
            command += ["bash", "-c", 'ulimit -f %d; exec \"$@\"' % fileseeklimit, "ulimit-helper"]
        # add environment
        command += ["env"]
        for k, v in environment_variables.items():
            command += ["%s=%s" % (k, v)]
    else:
        command = []
    command += args[:]


    # TODO: Dont even read in output longer than fileseeklimit. This might be most conveniently done by supplying a file like object instead of PIPE

    def prepare_subprocess():
        # create a new session for the spawned subprocess using os.setsid,
        # so we can later kill it and all children on timeout, taken from http://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
        os.setsid()
        # Limit the size of files created during execution.
        # Default value of filenumberlimit is 128.
        # In newer versions, R requires more to be started
        # (see comment in RscriptChecker.py),
        # even if it does not use it.
        resource.setrlimit(resource.RLIMIT_NOFILE, (filenumberlimit, filenumberlimit))
        if fileseeklimit is not None:
            resource.setrlimit(resource.RLIMIT_FSIZE, (fileseeklimitbytes, fileseeklimitbytes))
            if resource.getrlimit(resource.RLIMIT_FSIZE) != (fileseeklimitbytes, fileseeklimitbytes):
                raise ValueError(resource.getrlimit(resource.RLIMIT_FSIZE))
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT if error_to_output else subprocess.PIPE,
        cwd=working_directory,
        env=environment,
        preexec_fn=prepare_subprocess)

    timed_out = False
    oom_ed = False
    try:
        [output, error] = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        term_cmd = ["pkill", "-TERM", "-s", str(process.pid)]
        kill_cmd = ["pkill", "-KILL", "-s", str(process.pid)]
        if not unsafe and settings.USEPRAKTOMATTESTER:
            term_cmd = sudo_prefix + term_cmd
            kill_cmd = sudo_prefix + kill_cmd
        subprocess.call(term_cmd)
        time.sleep(5)
        subprocess.call(kill_cmd)
        [output, error] = process.communicate()
        #killpg(process.pid, signal.SIGKILL)

    if settings.USESAFEDOCKER and process.returncode == 23: #magic value
        timed_out = True

    if settings.USESAFEDOCKER and process.returncode == 24: #magic value
        oom_ed = True

    return [output.decode('utf-8'), error, process.returncode, timed_out, oom_ed]
