This is the source distribution of Praktomat, a programming course manager.

Resources
=========

In case of bugs or feature requests, please use the [Bug tracker]. There is
also a moderated [mailing list] for Praktomat administrators:
praktomat-users@lists.kit.edu.


General setup
=============

You need Python 3.5 and a recent version of pip. We also highly recommend to
use virtualenv so your system Python installation remains clean.

If you are having trouble with 

    pip install

and get a **No matching distribution found** or **Could not fetch URL** error, 
try adding -v to the command to get more information:

    pip install --upgrade -v pip

If you see an error like **There was a problem confirming the ssl certificate** or **tlsv1 alert protocol version or TLSV1_ALERT_PROTOCOL_VERSION**, you need to be connecting to PyPI with a newer TLS support library.

Reason: PyPI turned off support for TLS versions 1.0 and 1.1 in April 2018
   https://pyfound.blogspot.com/2017/01/time-to-upgrade-your-python-tls-v12.html

To fix this, it might help to run the following command:

    pip install -U pip virtualenv setuptools wheel urllib3[secure]

Prerequisites
============
  We recommend to run Praktomat within Apache, using Postgresql as
  database.

  On a Debian or Ubuntu System, install the packages

    postgresql
    apache2

  Praktomat requires some 3rd-Party libraries programs to run.
  On a Ubuntu/Debian System, these can be installed by installing the following packages:

    libpq-dev
    zlib1g-dev
    libmysqlclient-dev (or: default-libmysqlclient-dev)
    libsasl2-dev
    libssl-dev
    swig
    libapache2-mod-xsendfile (version 0.12; or install version 1.0 manually)
    libapache2-mod-wsgi-py3

    openjdk-11-jdk (or: openjdk-8-jdk)
    junit
    junit4
    dejagnu
    gcj-jdk (gcj compiler)
    r-base

    git-core

  If youre going to use Praktomat to check Haskell submissions, you will also require the packages:

    ghc libghc-test-framework-dev libghc-test-framework-hunit-dev libghc-test-framework-quickcheck2-dev

 For Checkstyle, we recommend getting checkstyle-all-4.4.jar

    http://sourceforge.net/projects/checkstyle/files/checkstyle/4.4/

 If you want your users to submit Isabelle theories, add the following line to
 /etc/mime.types:

    text/x-isabelle thy

Python 3.5
==========
  The Praktomat currently requires Python 3.5

  On Ubuntu 16.04, Python3.5 is installed by default,
  but you may need to install the packages

    python-setuptools
    python-psycopg2
    python-virtualenv

Developer setup
===============

Clone this repo and install the required python libs to either your system-wide
Python installation or inside a designated virtualenv (recommended).
The following describes a recommended setup using virtualenv.

```bash
git clone --recursive git://github.com/KITPraktomatTeam/Praktomat.git
virtualenv -p python3 --system-site-packages env/
. env/bin/activate
pip install -r Praktomat/requirements.txt
```

The initial database setup follows.

```bash
cd Praktomat
mkdir data
./src/manage-devel.py migrate --noinput
./src/manage-devel.py createsuperuser
```

Start the development server.

```bash
./src/manage-devel.py runserver
```


Deployment installation
=======================

Like for the development version, clone the Praktomat and install its dependencies:

```bash
git clone --recursive git://github.com/KITPraktomatTeam/Praktomat.git
virtualenv -p python3 --system-site-packages env/
. env/bin/activate
pip install -r Praktomat/requirements.txt
```

Now create a database. Using postgres on Ubuntu, this might work for creating
a database "praktomat_default". Also edit `pg_hba.conf` to allow the access.

```bash
sudo -u postgres createuser -DRS praktomat
sudo -u postgres createdb -O praktomat praktomat_default
```

Configure Praktomat in `Praktomat/src/settings/local.py`, which contains all settings and paths for your deployment system.

Create the upload directory, populate the database:

```bash
mkdir PraktomatSupport
./Praktomat/src/manage-local.py collectstatic --noinput --link
./Praktomat/src/manage-local.py migrate --noinput
```

It should now be possible to start the deployment server with:
```bash
./Praktomat/src/manage-local.py runserver
```
If you want to deploy the project using mod_wsgi in apache you could use `documentation/apache_praktomat_wsgi.conf` as a starting point. Don't forget to install `mod_xsendfile` to serve uploaded files.

Adding the first user
---------------------

If you use django for authentification, you might want to add a first user using

```bash
./Praktomat/src/manage-local.py createsuperuser
```

If you use single-sign-on via Shibboleth, you can already log in. After you have logged in, you can assign super user rights to yourself using

```bash
./Praktomat/src/manage-local.py makesuperuser --username=<the_user_name>
```

The username is visible under “View Account”; by default it is the e-mail address submitted by the Shibboleth server.

Update
======

1. update the source with git from github

2. backup your database (seriously!)

3. update the static files and the database:

```bash
./Praktomat/src/manage-local.py migrate --noinput
./Praktomat/src/manage-local.py collectstatic --noinput --link
```

Security
========

Besides the security provided by Java (via the Security Manager Profiles found
in `src/checker/scripts/`), the praktomat supports two way to insulate student
submissions from the system:

 * With `USEPRAKTOMATTESTER = True` in the settings, external commands are
   prefixed with `sudo -u tester --`. For this to work you need to add a user
   `tester` which is also a member of the default group of the user that runs
   the praktomat (usually `praktomat`).
 * With `USESAFEDOCKER = True`, external commands are prefixed with
   `safe-docker`, which you need to have installed. You can fetch it from
   http://github.com/nomeata/safe-docker

   For this to work you need to have a docker image named `safe-docker`
   installed, which needs to have all required dependencies installed. A
   suggested docker image is available in `docker-image`, so to get started simply run

        sudo docker build -t safe-docker docker-image

We recommend `USESAFEDOCKER`, as that is what we test in practice.

The Praktomat tries to limit the resources available to the student submissions:

 * The runtime of the submission can be limited (setting `TEST_TIMEOUT`)
 * The maximum amount of memory used can be limited (setting `TEST_MAXMEM`,
   only supported with `USESAFEDOCKER`).
 * The maximum size of a file produced by a user submission (setting
   `TEST_MAXFILESIZE`, currently not supported with `USESAFEDOCKER`, until
   http://stackoverflow.com/questions/25789425 is resolved)

At the time of writing, the amount of diskspace available to the user is
unlimited, which can probably be exploited easily.

jPlag integration
=================

Praktomat provides a rudimentary, but convenient integration of the plagiarism
detection program [jPlag](https://jplag.ipd.kit.edu/). Do enable this support, you have to do these two steps:

 * Download the latest [jPlag release](https://github.com/jplag/jplag/releases) (latest tested version: v2.12.1)
 * Copy the resulting `.jar` file somewhere on the Praktomat server.
 * In the settings, set `JPLAGJAR = /full/path/to/jplag.jar`


PhpBB integration
=================

To access the praktomat usersessions from an phpBB follow the instructions in `src/sessionprofile/phpbb/README.txt`.


[Bug tracker]: https://github.com/KITPraktomatTeam/Praktomat/issues
[mailing list]: https://www.lists.kit.edu/wws/info/praktomat-users
