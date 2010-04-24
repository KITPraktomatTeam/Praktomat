This is the source distribution of Praktomat, a programming course manager.

Installation 
============

1. download praktomat from svn (svn+ssh://user@ssh.info.uni-karlsruhe.de/ben/local/SVN/giffhorn/Django-Praktomat)  

2. run "python2.6 bootstrap.py" from praktomat root directory (Python < 2.6 is not supported!)

3. run "./bin/buildout" from praktomat root directory
	
4. reconfigure django settings in praktomat/src/praktomat/settings_local.py (http://docs.djangoproject.com/en/1.1/topics/settings/#topics-settings)

	- make sure your database accepts 'utf-8' encoding

5. run "./bin/praktomat syncdb" to populate the database with the required tables of 3rd party applications
	
6. run "./bin/praktomat migrate" to install the praktomat database tables
	
	- (optional) install some test data with "./bin/praktomat loaddata documentation/test_data.json" this will give you some users to play with
	Logins: user, tutor, trainer, admin (username=password)

7. it should now be possible to start the developmet server with "./praktomat runserver" or "./praktomat runserver_plus"

8. setup an administration account with "./bin/praktomat createsuperuser" if you haven't installed the test data which includes an "admin" account.

9. set up the domain name in the admin panel of the webapp

10. If you want to deploy the project using mod_wsgi in apache you could use documentation/apache_praktomat_wsgi.conf as a starting point


Update 
======

1. update the source with svn

2. update python dependencies with "./bin/buildout"

3. backup your database(seriously!) and run "./bin/praktomat syncdb" to install any new 3rd party tables as well as "./bin/praktomat migrate" to update praktomats tables