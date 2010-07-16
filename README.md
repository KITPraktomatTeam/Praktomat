This is the source distribution of Praktomat, a programming course manager.

Installation 
============

1. download praktomat from github (http://github.com/danielkleinert/Praktomat)  

2. run "python bootstrap.py" from praktomat root directory (Python < 2.7 is not supported!)

3. run "./bin/buildout" from praktomat root directory

4. create a database in utf-8 encoding. MySQL: "CREATE DATABASE Praktomat DEFAULT CHARACTER SET utf8" (http://docs.djangoproject.com/en/dev/topics/install/#database-installation)
	
5. reconfigure django settings in praktomat/src/praktomat/settings_local.py (http://docs.djangoproject.com/en/1.1/topics/settings/#topics-settings)

6. run "./bin/praktomat syncdb" to populate the database with the required tables of 3rd party applications
	
7. run "./bin/praktomat migrate" to install the praktomat database tables
	
	- (optional) install(also reset) a test database by running "./bin/praktomat install_demo_db", which copies the contents of "./examples/PraktomatSupport" to the folder 'UPLOAD_ROOT' configured in settings_local.py. 
	You need to change your database to the contained SQLite-database 'Database'.  
	Logins: userXY, tutorX, trainer, admin (password='demo') X in [1,3], Y in [1,5]

8. it should now be possible to start the developmet server with "./bin/praktomat runserver" or "./bin/praktomat runserver_plus"

9. setup an administration account with "./bin/praktomat createsuperuser" if you haven't installed the test data which includes an "admin" account.

10. set up the domain name in the admin panel of the webapp

11. If you want to deploy the project using mod_wsgi in apache you could use documentation/apache_praktomat_wsgi.conf as a starting point


Update 
======

1. update the source with git or svn from github

2. update python dependencies with "./bin/buildout"

3. backup your database(seriously!) and run "./bin/praktomat syncdb" to install any new 3rd party tables as well as "./bin/praktomat migrate" to update praktomats tables