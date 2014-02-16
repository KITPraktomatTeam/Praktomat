This is the source distribution of Praktomat, a programming course manager.

Resources
=========

In case of bugs or feature requests, please use the [Bug tracker]. There is
also a moderated [mailing list] for Praktomat administrators:
praktomat-users@lists.kit.edu.


General setup
=============

You need Python 2.7 and a recent version of pip. I also highly recommend to
use virtualenv so your system Python installation remains clean.

Prerequisites
============
  We recommend to run Praktomat within Apache, using Postgresql as
  database.

  On a Debian or Ubuntu System, install the packages

    postgresql
    apache2-mpm-worker	

  Praktomat requires some 3rd-Party libraries programs to run.
  On a Ubuntu/Debian System, these can be installed by installing the following packages:

    libpq-dev
    zlib1g-dev
    libmysqlclient-dev
    libsasl2-dev
    libssl-dev
    swig
    libapache2-mod-xsendfile
    libapache2-mod-wsgi

    sun-java6-jdk (from the "Canonical Parner" Repository)
    junit
    junit4
    dejagnu
    gcj-jdk (jfc-dump, for checking Submissions for use of javax.* etc)
    jclassinfo
   
    git-core

  If youre going to use Praktomat to check Haskell submissions, you will also require the packages:

    ghc libghc-test-framework-dev libghc-test-framework-hunit-dev libghc-test-framework-quickcheck2-dev

 For Checkstyle, we recommend getting checkstyle-all-4.4.jar  

    http://sourceforge.net/projects/checkstyle/files/checkstyle/4.4/

 If you want your users to submit Isabelle theories, add the following line to
 /etc/mime.types:

    text/x-isabelle thy

Python 2.7
==========
  The Praktomat currently requires Python 2.7

  On Ubuntu 11.04, Python2.7 is installed by default,
  but you may need to install the packages

    python2.7-dev
    python-setuptools
    python-psycopg2
    python-m2crypto
    python-virtualenv

Developer setup
===============

Clone this repo and install the required python libs to either your system-wide
Python installation or inside a designated virtualenv (recommended).
The following describes a recommended setup using virtualenv.

```bash
git clone --recursive git://github.com/KITPraktomatTeam/Praktomat.git
virtualenv --system-site-packages env/
. env/bin/activate
pip install -r Praktomat/requirements.txt
```

The initial database setup follows.

```bash
cd Praktomat
mkdir data
./src/manage-devel.py syncdb --noinput --migrate
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
virtualenv --system-site-packages env/
. env/bin/activate
pip install -r Praktomat/requirements.txt
```

Now create a database. Using postgres on Ubuntu, this might work for creating
a database "praktomat_default". Also edit `pg_hba.conf` to allow the access.

```bash
sudo -u postgres createuser -DRS praktomat
sudo -u postgres createdb -O praktomat praktomat_default
```
	
Configure Praktomat in `Praktomat/src/settings/local.py`, to set data base
names and paths.

Create the upload directory, populate the database and create a super user:

```bash
mkdir PraktomatSupport
./Praktomat/src/manage-local.py collectstatic --noinput --link
./Praktomat/src/manage-local.py syncdb --noinput --migrate
```

It should now be possible to start the developmet server with:
```bash
./Praktomat/src/manage-local.py runserver
```
If you want to deploy the project using mod_wsgi in apache you could use `documentation/apache_praktomat_wsgi.conf` as a starting point. Don't forget to install `mod_xsendfile` to serve uploaded files. 

Adding the first user
---------------------

If you use django for authentification, you might want to add a first user using

```bash
./Praktomat/src/manage-local.py createsuperuser -
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
./Praktomat/src/manage-local.py syncdb --noinput --migrate
./Praktomat/src/manage-local.py createsuperuser -
```

PhpBB integration 
=================

To access the praktomat usersessions from an phpBB folow the instructions in `src/sessionprofile/phpbb/README.txt`.


[Bug tracker]: https://github.com/KITPraktomatTeam/Praktomat/issues
[mailing list]: https://www.lists.kit.edu/wws/info/praktomat-users
