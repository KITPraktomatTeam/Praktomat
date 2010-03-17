

This is the source distribution of Praktomat, a programming course manager.


	Installation with buildout
==================================

1. download praktomat from svn (svn+ssh://user@ssh.info.uni-karlsruhe.de/ben/local/SVN/giffhorn/Django-Praktomat)  

2. run "python2.6 bootstrap.py" from praktomat root directory (Python < 2.6 is not supported!)

3. run "./bin/buildout" from praktomat root directory
	
4. reconfigure django settings in praktomat/src/praktomat/settings_local.py (http://docs.djangoproject.com/en/1.1/topics/settings/#topics-settings)

	4.1 make sure your database accepts 'utf-8' encoding

5. run "./bin/praktomat syncdb" to populate the database with the required tables
	(This will only install new tables and wont update existing ones. You can however reset all Tables with 'reset_db'.)
	
	5.1 install initial data with "./bin/praktomat loaddata src/praktomat/initial_data.json"
	
	5.2 (optional) install some test data with "./bin/praktomat loaddata documentation/test_data.json" this will give you some users to play with
	Logins: user, tutor, trainer, admin (username=password)

6. it should now be possible to start the developmet server with "./praktomat runserver" or "./praktomat runserver_plus"

7. setup an administration account with "./bin/praktomat createsuperuser" if you haven't installed the test data which includes an "admin" account.

8. set up the domain name in the admin panel of the webapp

9. If you want to deploy the project using mod_wsgi in apache you could use documentation/apache_praktomat_wsgi.conf as a starting point
