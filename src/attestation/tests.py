from datetime import datetime, timedelta

from utilities.TestSuite import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

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
			self.failUnlessEqual(response.status_code, 200)

		def test_get_new_attestation(self):
			response = self.client.get(reverse('new_attestation_for_solution', args=[self.solution.id]), follow=True)
			self.failUnlessEqual(response.status_code, 200)

		def test_get_edit_attestation(self):
			response = self.client.get(reverse('edit_attestation', args=[self.attestation.id]))
			self.failUnlessEqual(response.status_code, 200)

		def test_post_edit_attestation(self):
			response = self.client.post(reverse('edit_attestation', args=[self.attestation.id]), data={
								u'attestfiles-TOTAL_FORMS': u'0',
								u'attestfiles-INITIAL_FORMS': u'0',
								u'ratingresult-TOTAL_FORMS': u'0',
								u'ratingresult-INITIAL_FORMS': u'0',
							}, follow=True)
			self.assertRedirectsToView(response, 'view_attestation')

		def test_get_view_attestation(self):
			response = self.client.get(reverse('view_attestation', args=[self.attestation.id]))
			self.failUnlessEqual(response.status_code, 200)

		def test_post_view_attestation(self):
			response = self.client.post(reverse('view_attestation', args=[self.attestation.id]),  data={
								u'final': True,
							}, follow=True)
			self.assertRedirectsToView(response, 'attestation_list')

class TestTrainerViews(TestCase):
		def setUp(self):
			self.client.login(username='trainer', password='demo')

		def tearDown(self):
			pass

		def test_get_raiting_overview(self):
			response = self.client.get(reverse('rating_overview'))
			self.failUnlessEqual(response.status_code, 200)

		def test_post_raiting_overview(self):
			response = self.client.post(reverse('rating_overview'), data={
								u'form-TOTAL_FORMS': 1,
								u'form-INITIAL_FORMS': 1,
								u'form-0-user_ptr': 1,
								u'form-0-final_grade:': u'',
							})
			self.failUnlessEqual(response.status_code, 200)

		def test_rating_export(self):
			response = self.client.get(reverse('rating_export'))
			self.failUnlessEqual(response.status_code, 200)
