from datetime import datetime, timedelta

from utilities.TestSuite import TestCase
from django.test.client import Client
from django.urls import reverse

from solutions.models import Solution
from tasks.models import Task
from attestation.models import Attestation

class TestViews(TestCase):
        def setUp(self):
            self.client.login(username='tutor', password='demo')
            self.task = Task.objects.all()[0]
            self.task.submission_date = datetime.now() - timedelta(hours=1)
            self.task.save()
            self.task.check_all_final_solutions()
            self.solution = Solution.objects.all()[0]
            self.attestation = Attestation.objects.all()[0]


        def tearDown(self):
            pass

        def test_get_attestation_list(self):
            response = self.client.get(reverse('attestation_list', args=[self.task.id]))
            self.assertEqual(response.status_code, 200)

        def test_get_new_attestation(self):
            response = self.client.get(reverse('new_attestation_for_solution', args=[self.solution.id]), follow=True)
            self.assertEqual(response.status_code, 200)

        def test_get_edit_attestation(self):
            response = self.client.get(reverse('edit_attestation', args=[self.attestation.id]))
            self.assertEqual(response.status_code, 200)

        def test_post_edit_attestation(self):
            response = self.client.post(reverse('edit_attestation', args=[self.attestation.id]), data={
                                'attestfiles-TOTAL_FORMS': '0',
                                'attestfiles-INITIAL_FORMS': '0',
                                'ratingresult-TOTAL_FORMS': '0',
                                'ratingresult-INITIAL_FORMS': '0',
                            }, follow=True)
            self.assertRedirectsToView(response, 'view_attestation')

        def test_get_view_attestation(self):
            response = self.client.get(reverse('view_attestation', args=[self.attestation.id]))
            self.assertEqual(response.status_code, 200)

        def test_post_view_attestation(self):
            response = self.client.post(reverse('view_attestation', args=[self.attestation.id]),  data={
                                'final': True,
                            }, follow=True)
            self.assertRedirectsToView(response, 'attestation_list')

class TestTrainerViews(TestCase):
        def setUp(self):
            self.client.login(username='trainer', password='demo')

        def tearDown(self):
            pass

        def test_get_raiting_overview(self):
            response = self.client.get(reverse('rating_overview'))
            self.assertEqual(response.status_code, 200)

        def test_post_raiting_overview(self):
            response = self.client.post(reverse('rating_overview'), data={
                                'form-TOTAL_FORMS': 1,
                                'form-INITIAL_FORMS': 1,
                                'form-0-user_ptr': 1,
                                'form-0-final_grade:': '',
                            })
            self.assertEqual(response.status_code, 200)

        def test_rating_export(self):
            response = self.client.get(reverse('rating_export'))
            self.assertEqual(response.status_code, 200)
