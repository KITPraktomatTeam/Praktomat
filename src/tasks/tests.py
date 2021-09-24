from os.path import dirname, join
from datetime import datetime, timedelta

from utilities.TestSuite import TestCase
from django.urls import reverse

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
        self.assertEqual(response.status_code, 200)

    def test_get_task_detail(self):
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

class TestStaffViews(TestCase):
    def setUp(self):
        self.client.login(username='trainer', password='demo')
        self.task = Task.objects.all()[0]

    def tearDown(self):
        pass

    def test_get_task_import(self):
        response = self.client.get(reverse('admin:task_import'))
        self.assertEqual(response.status_code, 200)

    def test_post_task_import(self):
        path = join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'AMI', 'TaskExport.zip')
        with open(path, 'rb') as f:
            response = self.client.post(reverse('admin:task_import'), data={
                               'file': f,
                               'is_template': True,
                            }, follow=True)
        self.assertRedirectsToView(response, 'changelist_view')

    def test_get_model_solution(self):
        response = self.client.get(reverse('model_solution', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_model_solution(self):
        with open(join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'AMI', 'ModelSolution(flat).zip'), 'rb') as f:
            response = self.client.post(reverse('model_solution', args=[self.task.id]), data={
                                'solutionfile_set-INITIAL_FORMS': '0',
                                'solutionfile_set-TOTAL_FORMS': '3',
                                'solutionfile_set-0-file': f
                            })
        self.assertNotContains(response, 'error_list')

    def test_task_export(self):
        response = self.client.post(reverse('admin:tasks_task_changelist'), data={
                            '_selected_action': 1,
                            'action': 'export_tasks'
                        })
        self.assertEqual(response.status_code, 200)

    def test_task_run_all_checker(self):
        # needs to be expired first
        self.task.submission_date = datetime.now() - timedelta(hours=2)
        self.task.save()

        # TODO: Create checker for test task!
        response = self.client.post(reverse('admin:tasks_task_changelist'), data={
                            '_selected_action': self.task.pk,
                            'action': 'run_all_checkers'
                        }, follow=True)
        self.task.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.task.all_checker_finished)

    def test_task_run_all_checker_parallel(self):
        with self.settings(NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL=4):
            self.test_task_run_all_checker()
