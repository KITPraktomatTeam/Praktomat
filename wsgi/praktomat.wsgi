#!/usr/bin/env python3
import os
import mod_wsgi
from os.path import join, dirname, basename

# For allowing more flexibility and reduce merge conflicts in Praktomat settings:
# As mentioned in https://github.com/KITPraktomatTeam/Praktomat/pull/279
# it is possible to use a settings file to configure Praktomat
# which is not src/settings/local.py, src/settings/test.py or src/settings/devel.py
# and tell apache in its config file how it is named:
# For instance with
#       SetEnv DJANGO_SETTINGS_MODULE settings.own
# In Praktomat macro for apache, see documentation/apache_praktomat_wsgi.conf,
# which could copied into /etc/apache2/sites-enabled/default-ssl.conf,
# there is the option process-group for WSGIScriptAlias
# and the first parameter as name for WSGIDaemonProcess
# both are set to the value "local_$id".
# If DJANGO_SETTINGS_MODULE is not set i.e. via SetEnv for apache,
# than we use the value of process-group to determine the required value for DJANGO_SETTINGS_MODULE.
# If the value for process-group is not available, i.e. while running a unit test against praktomat.wsgi,
# than we fall back to "local".
# If DJANGO_SETTINGS_MODULE is allready defined, than we do not overwrite it.
# DJANGO_SETTINGS_MODULE can be created via SetEnv for apache
# or via calling ./src/manage-test.py or ./src/manage-devel.py or ./src/manage-local.py

try:
    from mod_wsgi import process_group
except ImportError:
    settings_module = 'local'
else:
    settings_module = str(repr(process_group)).strip("'").strip("\"").strip().split("_",1)[0] # We take the substring infront of the underscore, or all if no underscore is there.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.%s' % (settings_module)) # only set DJANGO_SETTINGS_MODULE if it is not setted at moment

import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

import pathlib

if PY2 :
    env_lib_path = pathlib.Path(join(dirname(dirname(dirname(__file__))), "env", "lib"))
    subdirs = [str(p) for p in env_lib_path.iterdir() if p.is_dir()]
    python_path = [p for p in subdirs if basename(p).startswith("python2.")][0]

if PY3 :
    env_lib_path = pathlib.Path(join(dirname(dirname(dirname(__file__))), "env", "lib"))
    subdirs = [str(p) for p in env_lib_path.iterdir() if p.is_dir()]
    python_path = [p for p in subdirs if basename(p).startswith("python3.")][0]

import site
site.addsitedir(join(python_path, "site-packages"))

sys.path.append(join(dirname(dirname(__file__)), "src"))

import warnings
from django.core.cache import CacheKeyWarning
warnings.simplefilter("ignore", CacheKeyWarning)

import resource
def set_to_hard(res):
    (s,h) = resource.getrlimit(res)
    resource.setrlimit(res,(h,h))
set_to_hard(resource.RLIMIT_AS)
set_to_hard(resource.RLIMIT_NPROC)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# vim:ft=python
