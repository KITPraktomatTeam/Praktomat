# -*- coding: utf-8 -*-

import os
from os.path import *
import time
import subprocess
import signal
from six import PY2
if PY2:
    import subprocess32 as subprocess
import resource
import psutil

from copy import deepcopy

from django.conf import settings

# found at http://stackoverflow.com/questions/1230669/subprocess-deleting-child-processes-in-windows
# should work for linux, too
# TODO: should kill child or grandchild processes, but didn't if they are running as other user;
#       wherefor it is necessary to use "ulimit -t 60" command in shell-scripts called by praktomat checkers:
#       forcing script exit with error after 60 seconds
def kill_proc_tree(pid, including_parent=False):
	parent = psutil.Process(pid)
	# just for debugging in development vm
        #f = open('workfile.rh', 'a', 0)
	f = None
	if f is not None:
		f.write("\n inside kill_proc_tree : " +str(parent.pid()) +" :"  +str(parent.cmdline())+"\n")

	children = parent.children(recursive=True)
	for child in children:
		if f is not None:
			f.write("\n try kill: "+str(child.pid())+":"+str(child.cmdline())+"\n")
		child.kill()
		if f is not None:
			f.write("\n kill returned\n ")
	psutil.wait_procs(children, timeout=5)
	if including_parent:
		parent.kill()
		parent.wait(5)

def execute_arglist(args, working_directory, environment_variables={}, timeout=None, maxmem=None, fileseeklimit=None, extradirs=[], unsafe=False, error_to_output=True, filenumberlimit=128):
    """ Wrapper to execute Commands with the praktomat testuser. Excpects Command as list of arguments, the first being the execeutable to run. """
    assert isinstance(args, list)

    command = args[:]

    environment = os.environ
    environment.update(environment_variables)
    if fileseeklimit is not None:
        fileseeklimitbytes = fileseeklimit * 1024

    sudo_prefix = ["sudo", "-E", "-u", "tester"]

    # Limit the size of files created during execution.
    # In newer versions, R requires more to be started
    # (see comment in RscriptChecker.py),
    # even if it does not use it.
    prlimit_prefix = ['prlimit', '--nofile=%d' % filenumberlimit]
    if fileseeklimit is not None:
        prlimit_prefix += ['--fsize=%d' % fileseeklimitbytes]

    command = prlimit_prefix

    if unsafe:
        pass
    elif settings.USEPRAKTOMATTESTER:
        #command = sudo_prefix
        #fixed: 22.11.2016, Robert Hartmann , H-BRS
        command += deepcopy(sudo_prefix)
    elif settings.USESAFEDOCKER:
        command += ["sudo", "safe-docker"]
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

    command += args[:]

    # TODO: Dont even read in output longer than fileseeklimit. This might be most conveniently done by supplying a file like object instead of PIPE

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT if error_to_output else subprocess.PIPE,
        cwd=working_directory,
        env=environment,
        start_new_session=True)

    timed_out = False
    oom_ed = False
    try:
        [output, error] = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
		# http://bencane.com/2014/04/01/understanding-the-kill-command-and-how-to-terminate-processes-in-linux/
        term_cmd = ["pkill", "-TERM", "-s", str(process.pid)]
        int_cmd  = ["pkill","-INT","-s",str(process.pid)]
        hup_cmd  = ["pkill","-HUP","-s",str(process.pid)]
        kill_cmd = ["pkill", "-KILL", "-s", str(process.pid)]
        if not unsafe and settings.USEPRAKTOMATTESTER:
            term_cmd = sudo_prefix + term_cmd
            int_cmd = sudo_prefix + int_cmd
            hup_cmd = sudo_prefix + hup_cmd
            kill_cmd = sudo_prefix + kill_cmd
        subprocess.call(term_cmd)
        time.sleep(5)
        subprocess.call(int_cmd)
        time.sleep(9)
        subprocess.call(hup_cmd)
        time.sleep(5)
        subprocess.call(kill_cmd)
        time.sleep(5)
        if process.poll() is None:
            #if we are here, than we retry to kill the subprocesses in an other way
            kill_proc_tree(pid=process.pid)
            time.sleep(5)
            process.kill()
        [output, error] = process.communicate()
        #killpg(process.pid, signal.SIGKILL)

    if settings.USESAFEDOCKER and process.returncode == 23: #magic value
        timed_out = True

    if settings.USESAFEDOCKER and process.returncode == 24: #magic value
        oom_ed = True

    return [output.decode('utf-8'), error, process.returncode, timed_out, oom_ed]
