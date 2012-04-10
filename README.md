This is the source distribution of Praktomat, a programming course manager.

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
    libmysqlclient-dev
    libsasl2-dev
    libssl-dev
    swig
    libapache2-mod-xsendfile

    sun-java6-jdk (from the "Canonical Parner" Repository)
    junit
    dejagnu
    gcj-jdk (jfc-dump, for checking Submissions for use of javax.* etc)
   
    git-core

 For Checkstyle, we recommend getting checkstyle-all-4.4.jar  

    http://sourceforge.net/projects/checkstyle/files/checkstyle/4.4/


Python 2.7
==========
  Unfortunately, Praktomat currently requires Python 2.7

  On Ubuntu 11.04, Python2.7 is installed by default,
  but you may need to install the packages

    python2.7-dev
    python-setuptools
    python-psycopg2
    
    sudo easy_install -U setuptools

  On Linux-Distributions (Ubuntu 10.4 LTS, Debian squeeze) that 
  ship with Python 2.6, we recommend to compile and install
  python 2.7 manually from source, by installing required packages with:

    sudo apt-get build-dep python
    sudo apt-get install libdb4.8-dev libgdbm-dev  

  and then something like:

    wget http://www.python.org/ftp/python/2.7.1/Python-2.7.1.tar.bz2
    tar xjf Python-2.7.1.tar.bz2
    cd Python-2.7.1/
    ./configure --enable-shared
    make 
    make altinstall

  Make sure to use this binary when bootstrapping praktomat in 
  the Installation Step 2: 

    python2.7 bootstrap.py
 
mod_wsgi
========
  If you want to run praktomat from within Apachhe, you will need mod_wsgi.
  On Linux-Distributions that ship with Python 2.7 per default, install
  the package

    libapache2-mod-wsgi


  If you compiled Python 2.7 manually, you have to compile
  and install mod_wsgi manually, as well. Get the source from
    http://code.google.com/p/modwsgi/
  and make sure to configure it similiarly to:

    ./configure --with-python=/usr/local/bin/python2.7


 


Installation 
============

1. Clone praktomat from github including submodules: 

        git clone --recursive git://github.com/danielkleinert/Praktomat.git

    If your git version does not support the `--recursive` option:

     1. Clone praktomat *without* submodules: `git clone git://github.com/danielkleinert/Praktomat.git`
     2. From the praktomat root directory,            run `git submodule init` and then `git submodule update`
     3. From the subdirectory `media/frameworks/ace`, run `git submodule init` and then `git submodule update`

2. Run `python bootstrap.py` from the praktomat root directory. (Python < 2.7 is not supported!)

3. Run `./bin/buildout` from praktomat root directory. 
   You need to have MySQL and PostgresSQL installed - otherwise the packages 'MySQL-python' or 'psycopg2' won't install. You can safely outcomment the corresponding package in setup.py if you'll only use the other database.  (Postgres in OSX: make shure pg_config is found: PATH=$PATH:/Library/PostgreSQL/8.4/bin/)

4. Create a database in utf-8 encoding. 

    MySQL: `CREATE DATABASE Praktomat DEFAULT CHARACTER SET utf8` (http://docs.djangoproject.com/en/dev/topics/install/#database-installation)

    Using postgres on Ubuntu, this might work for creating a database "praktomat_default"

        sudo -u postgres createuser -DRS praktomat

        sudo -u postgres createdb -O praktomat praktomat_default
	
5. Reconfigure django settings in `Praktomat/src/settings_local.py` (http://docs.djangoproject.com/en/1.3/topics/settings/#topics-settings)

6. Run `./bin/praktomat syncdb` to populate the database with the required tables of 3rd party applications. If prompted don't create a superuser as required tables will be created in the next step.
	
7. Run `./bin/praktomat migrate` to install the praktomat database tables.
	* (optional) Install(also reset) a test database by running `./bin/praktomat install_demo_db`, which copies the contents of `./examples/PraktomatSupport` to the folder `UPLOAD_ROOT` configured in `settings_local.py`. 
	  You need to change your database to the contained SQLite-database 'Database'.  
	  Logins: userXY, tutorX, trainer, admin (password='demo') X in [1,3], Y in [1,5]

8. It should now be possible to start the developmet server with `./bin/praktomat runserver` or `./bin/praktomat runserver_plus`

9. Setup an administration account with `./bin/praktomat createsuperuser` if you haven't installed the test data which includes an "admin" account.

10. If you want to deploy the project using mod_wsgi in apache you could use `documentation/apache_praktomat_wsgi.conf` as a starting point. Don't forget to install `mod_xsendfile` to serve uploaded files. 


Update 
======

1. update the source with git or svn from github

2. update python dependencies with `./bin/buildout`

3. backup your database(seriously!) and run `./bin/praktomat syncdb` to install any new 3rd party tables as well as `./bin/praktomat migrate` to update praktomats tables


PhpBB integration 
=================

To access the praktomat usersessions from an phpBB folow the instructions in `src/sessionprofile/phpbb/README.txt`.

