# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test.runner import DiscoverRunner
from django.test import TestCase as DjangoTestCase
from django.conf import settings
from os.path import dirname, join
from shutil import rmtree

class TestSuiteRunner(DiscoverRunner):
    testSuiteUploadRoot = join(settings.UPLOAD_ROOT, 'TestSuite')

    def setup_test_environment(self, **kwargs):
        """ Change the upload root to not mess up the production folder """
        super(TestSuiteRunner, self).setup_test_environment(**kwargs)
        settings.UPLOAD_ROOT = self.testSuiteUploadRoot
        # storage object is lazy and is not updated by simply updating the settings
        from django.core.files.storage import default_storage
        default_storage.location = self.testSuiteUploadRoot

    def setup_databases(self, **kwargs):
        """ Prefill database with some testdata. Rollbacks ensure that the database is in the state after create_test_data().
        Rollbacks need to be supported by the database otherwise the db will be flushed after every test.
        This is much quicker than creating everything in setUp() and more flexible than fixtures as you can use files. """
        x = super(TestSuiteRunner, self).setup_databases(**kwargs)
        create_test_data()
        return x

    def teardown_test_environment(self, **kwargs):
        super(TestSuiteRunner, self).teardown_test_environment(**kwargs)
        try:
            rmtree(self.testSuiteUploadRoot)
        except:
            pass



class TestCase(DjangoTestCase):

    def assertRedirectsToView(self, response, view):
        """ Asserts whether the request was redirected to a specific view function. """
        from six import PY2
        if PY2:
            from urlparse import urlparse
        else:
            from urllib.parse import urlparse
        from django.urls import resolve
        self.assertTrue(hasattr(response, 'redirect_chain'),
                        msg="Please use client.get(...,follow=True) with assertRedirectsToView")
        self.assertTrue(len(response.redirect_chain) > 0,
                        msg="No redirection found")
        url = response.redirect_chain[-1][0]
        self.assertEqual(resolve(urlparse(url)[2])[0].__name__, view)



from accounts.models import User, Tutorial
from django.contrib.auth.models import Group
from tasks.models import Task
from solutions.models import Solution, SolutionFile
from attestation.models import Attestation

from datetime import datetime, timedelta

from django.core.files import File

def create_test_data():
    """ Fills the test db with objects needed in the unit tests. """

    # Users & Tutorials
    trainer = User.objects.create_user('trainer', 'trainer@praktomat.com', 'demo')
    trainer.groups.add(Group.objects.get(name='Trainer'))
    trainer.is_staff = True
    trainer.is_superuser = True
    trainer.save()

    tutor = User.objects.create_user('tutor', 'trainer@praktomat.com', 'demo')
    tutor.groups.add(Group.objects.get(name='Tutor'))

    tutorial = Tutorial.objects.create(name='Tutorial 1')
    tutorial.tutors.add(tutor)

    user = User.objects.create_user('user', 'user@praktomat.com', 'demo')
    user.groups.add(Group.objects.get(name='User'))
    user.tutorial = tutorial
    user.mat_number = 11111
    user.save()

    # Tasks
    task = Task.objects.create(
            title = 'Test task',
            description = 'Test description.',
            publication_date = datetime.now() - timedelta(hours=5),
            submission_date =  datetime.now() + timedelta(hours=5)
            #model_solution
            #all_checker_finished = False
            #final_grade_rating_scale =
        )

    # Solutions
    solution = Solution.objects.create(    task = task, author = user )

    solution_file = SolutionFile(solution = solution)
    with open(join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'GGT', 'solutions', 'GgT.java')) as fd:
        solution_file.file.save('GgT.java', File(fd))

    # Attestation
    attestation = Attestation.objects.create(solution = solution, author=tutor) # final, published

def dump(obj):
    """ Kinda like obj.__meta__ but shows more, very usefull for testcase debugging. """
    for attr in dir(obj):
        print("obj.%s = %s" % (attr, getattr(obj, attr)))
