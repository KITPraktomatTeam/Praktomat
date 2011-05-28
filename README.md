This is the source distribution of Praktomat, a programming course manager.

Installation 
============

1. Clone praktomat from github including submodules: "git clone --recursive git://github.com/danielkleinert/Praktomat.git"

   If your git version does not support the "--recursive" option:
     1.a) Clone praktomat "without" submodules: "git clone git://github.com/danielkleinert/Praktomat.git"
     1.b) From the praktomat root directory,            run "git submodule init" and then "git submodule update"
     1.c) From the subdirectory "media/frameworks/ace", run "git submodule init" and then "git submodule update"

2. Run "python bootstrap.py" from the praktomat root directory. (Python < 2.7 is not supported!)

3. Run "./bin/buildout" from praktomat root directory. You need to have MySQL and PostgresSQL installed - otherwise the packages 'MySQL-python' or 'psycopg2' won't install. You can safely outcomment the corresponding package in setup.py if you'll only use the other database.  (Postgres in OSX: make shure pg_config is found: PATH=$PATH:/Library/PostgreSQL/8.4/bin/)

4. Create a database in utf-8 encoding. MySQL: "CREATE DATABASE Praktomat DEFAULT CHARACTER SET utf8" (http://docs.djangoproject.com/en/dev/topics/install/#database-installation)
	
5. Reconfigure django settings in praktomat/src/praktomat/settings_local.py (http://docs.djangoproject.com/en/1.1/topics/settings/#topics-settings)

6. Run "./bin/praktomat syncdb" to populate the database with the required tables of 3rd party applications. If prompted don't create a superuser as required tables will be created in the next step.
	
7. Run "./bin/praktomat migrate" to install the praktomat database tables.
	
	- (optional) Install(also reset) a test database by running "./bin/praktomat install_demo_db", which copies the contents of "./examples/PraktomatSupport" to the folder 'UPLOAD_ROOT' configured in settings_local.py. 
	You need to change your database to the contained SQLite-database 'Database'.  
	Logins: userXY, tutorX, trainer, admin (password='demo') X in [1,3], Y in [1,5]

8. It should now be possible to start the developmet server with "./bin/praktomat runserver" or "./bin/praktomat runserver_plus"

9. Setup an administration account with "./bin/praktomat createsuperuser" if you haven't installed the test data which includes an "admin" account.

10. If you want to deploy the project using mod_wsgi in apache you could use documentation/apache_praktomat_wsgi.conf as a starting point. Don't forget to install mod_xsendfile to serve uploaded files. 


Update 
======

1. update the source with git or svn from github

2. update python dependencies with "./bin/buildout"

3. backup your database(seriously!) and run "./bin/praktomat syncdb" to install any new 3rd party tables as well as "./bin/praktomat migrate" to update praktomats tables
