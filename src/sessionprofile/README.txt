Django Logins for phpBB
=======================

This project contains the code required to set up your site so that people
can log in using Django authentication, and then post to a phpBB forum without
having to log in again.  As such it is (obviously) dependent on Django and
phpBB.

-------------------------------------------------------------------------------

WARNING: the Django username is used as the phpBB username by this module.
This means that once this code is in use, anyone who can log into Django with a
given username can log in as the person with the same username on your phpBB
site.  You should check that there are no clashes BEFORE installing the code.
In particular, we recommend you make sure that usernames used by the
administrators of your phpBB site are registered Django users, and that they
are people you really would like to have as phpBB administrators!

-------------------------------------------------------------------------------

The codebase comprises two sections:

* The django code.  This is a Django app called sessionprofile.  Its README.txt
  tells you how to add it to your project.  We recommend you look at this bit
  first.

* The phpBB code.  This needs to be installed in your phpBB directory; details
  are in the included README.txt file.

Once you have both installed, you should be up and running.

All code and documentation is made available under an MIT license.


-------------------------------------------------------------------------------

Any problems?  Let us know at

    django-php-auth@resolversystems.com
