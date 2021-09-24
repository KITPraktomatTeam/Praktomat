from os.path import dirname, join
from datetime import datetime, timedelta

from utilities.TestSuite import TestCase
from django.test.client import Client
from django.urls import reverse

from solutions.models import Solution
from tasks.models import Task

class TestViews(TestCase):
    def setUp(self):
        self.client.login(username='user', password='demo')
        self.task = Task.objects.all()[0]

    def tearDown(self):
        pass

    def test_get_solution_list(self):
        response = self.client.get(reverse('solution_list', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_solution(self):
        path = join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'AMI', 'ModelSolution(flat).zip')
        with open(path, 'rb') as f:
            response = self.client.post(reverse('solution_list', args=[self.task.id]), data={
                                'solutionfile_set-INITIAL_FORMS': '0',
                                'solutionfile_set-TOTAL_FORMS': '3',
                                'solutionfile_set-0-file': f
                            }, follow=True)
        self.assertRedirectsToView(response, 'solution_detail')

    def test_post_solution_expired(self):
        self.task.submission_date = datetime.now() - timedelta(hours=3)
        self.task.save()

        path = join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'AMI', 'ModelSolution(flat).zip')
        with open(path, 'rb') as f:
            response = self.client.post(reverse('solution_list', args=[self.task.id]), data={
                                'solutionfile_set-INITIAL_FORMS': '0',
                                'solutionfile_set-TOTAL_FORMS': '3',
                                'solutionfile_set-0-file': f
                            }, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_solution(self):
        response = self.client.get(reverse('solution_detail', args=[self.task.solution_set.all()[0].id]))
        self.assertEqual(response.status_code, 200)


def test_concurrently(times):
    """
    Add this decorator to small pieces of code that you want to test
    concurrently to make sure they don't raise exceptions when run at the
    same time.  E.g., some Django views that do a SELECT and then a subsequent
    INSERT might fail when the INSERT assumes that the data has not changed
    since the SELECT.
    """
    def test_concurrently_decorator(test_func):
        def wrapper(*args, **kwargs):
            exceptions = []
            import threading
            def call_test_func():
                try:
                    test_func(*args, **kwargs)
                except Exception as e:
                    exceptions.append(e)
                    raise
            threads = []
            for i in range(times):
                threads.append(threading.Thread(target=call_test_func))
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            if exceptions:
                raise Exception('test_concurrently intercepted %s exceptions: %s' % (len(exceptions), exceptions))
        return wrapper
    return test_concurrently_decorator

        # Use like this:
        # Transaction in djangos testcase results in an deadlock so use pythons
        #class MyTest(TestCase):
        #        def testRegistrationThreaded(self):
        #                url = reverse('toggle_registration')
        #                @test_concurrently(15)
        #                def toggle_registration():
        #                        # perform the code you want to test here; it must be thread-safe
        #                        # (e.g., each thread must have its own Django test client)
        #                        c = Client()
        #                        c.login(username='user@example.com', password='abc123')
        #                        response = c.get(url)
        #                toggle_registration()


#from unittest import TestCase as ConcurrentTestCase
#class ConcurentTest(ConcurrentTestCase):
        #""" Will probably result in an error as not all db connections will be closed on table destruction """
        #def setUp(self):
            #self.task = Task.objects.all()[0]

        #def tearDown(self):
            #pass

        #def test_post_solution_concurrently(self):
                #url = reverse('solution_list', args=[self.task.id])
                #@test_concurrently(20)
                #def run():
                        #f = open('/Users/halluzinativ/untitled.c','r')
                        #client = Client()
                        #client.login(username='user', password='demo')
                        #response = client.post(url, follow=True, data={
                                #u'solutionfile_set-INITIAL_FORMS': u'0',
                                #u'solutionfile_set-TOTAL_FORMS': u'3',
                                #u'solutionfile_set-0-file': f
                            #})
                        #self.failUnlessEqual(response.status_code, 200)
                #run()
