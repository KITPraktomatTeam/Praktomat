from os.path import dirname, join
from datetime import datetime, timedelta

from utilities.TestSuite import TestCase
from django.core.urlresolvers import reverse

from solutions.models import Solution
from tasks.models import Task

class TestUserViews(TestCase):
		def setUp(self):
			self.client.login(username='user', password='demo')
			self.task = Task.objects.all()[0]

		def tearDown(self):
			pass
		
		def test_get_task_list(self):
			response = self.client.get(reverse('task_list'))
			self.failUnlessEqual(response.status_code, 200)

		def test_get_task_detail(self):
			response = self.client.get(reverse('task_detail', args=[self.task.id]))
			self.failUnlessEqual(response.status_code, 200)

class TestStaffViews(TestCase):
		def setUp(self):
			self.client.login(username='trainer', password='demo')
			self.task = Task.objects.all()[0]

		def tearDown(self):
			pass
		
		def test_get_task_import(self):
			response = self.client.get(reverse('admin:task_import'))
			self.failUnlessEqual(response.status_code, 200)

		def test_post_task_import(self):
			path = join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'AMI', 'TaskExport.zip')
			f = open(path, 'r')
			response = self.client.post(reverse('admin:task_import'), data={
								u'file': f
							}, follow=True)
			self.assertRedirectsToView(response, 'changelist_view')

		def test_get_model_solution(self):
			response = self.client.get(reverse('model_solution', args=[self.task.id]))
			self.failUnlessEqual(response.status_code, 200)

		def test_post_model_solution(self):
			f = open(join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'AMI', 'ModelSolution(flat).zip'), 'r')
			response = self.client.post(reverse('model_solution', args=[self.task.id]), data={
								u'solutionfile_set-INITIAL_FORMS': u'0',
								u'solutionfile_set-TOTAL_FORMS': u'3',
								u'solutionfile_set-0-file': f
							})
			self.assertNotContains(response, 'error_list')

                def test_task_export(self):
                        response = self.client.post(reverse('admin:tasks_task_changelist'), data={
                                                        u'_selected_action': 1,
                                                        u'action': u'export_tasks'
                                                })
                        self.failUnlessEqual(response.status_code, 200)

                def test_task_run_all_checker(self):
                        # needs to be expired first
                        self.task.submission_date = datetime.now() - timedelta(hours=2)
                        self.task.save()

                        # TODO: Create checker for test task!
                        response = self.client.post(reverse('admin:tasks_task_changelist'), data={
                                                        u'_selected_action': self.task.pk,
                                                        u'action': u'run_all_checkers'
                                                }, follow=True)
                        self.task.refresh_from_db()
                        self.failUnlessEqual(response.status_code, 200)
                        self.failUnless(self.task.all_checker_finished)

                def test_task_run_all_checker_parallel(self):
                    with self.settings(NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL=4):
                        self.test_task_run_all_checker()
