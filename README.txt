

This is the source distribution of Praktomat, a programming course manager.


	Installation with buildout
==================================


1. install setuptools (pypi.python.org/pypi/setuptools)

2. download praktomat from svn (svn+ssh://user@ssh.info.uni-karlsruhe.de/ben/local/SVN/giffhorn/Django-Praktomat)  

3. run "python bootstrap.py" from praktomat root directory

4. run "./bin/buildout" from praktomat root directory

	4.1 it should now be possible to start the developmet server with "./praktomat runserver" or "./praktomat runserver_plus"
		localhost:8000 should show an errorpage
	
5. reconfigure django settings in praktomat/src/praktomat/settings_local.py (http://docs.djangoproject.com/en/1.1/topics/settings/#topics-settings)

6. run "./bin/praktomat syncdb" to populate the database with the required tables
	(This will only install new tables and wont update existing ones. You can however reset all Tables with 'reset_db'.)

7. (optional) install some test data with "./bin/praktomat loaddata documentation/test_data.json" this will give you some users to play with
	Logins: user, tutor, trainer, admin (username=password)

8. setup an administration account with "./bin/praktomat createsuperuser" if you skipped step 7.

9. set up the domain name in the admin panel of the webapp

10. If you want to deploy the project using mod_wsgi in apache you could use documentation/apache_praktomat_wsgi.conf as a starting point
