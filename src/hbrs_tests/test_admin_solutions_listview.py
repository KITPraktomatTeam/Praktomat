# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from django.contrib.admin.sites import AdminSite

from accounts.models import User
from tasks.models import Task

from solutions.models import Solution
from solutions.admin import SolutionAdmin


class ModelSolutionAdminTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # ö , ä , ü = 0xC3 0xB6 , 0xC3 0xA4 , 0xC3 0xBC : letters coded in UTF8
        cls.umlautStudent = User.objects.create_user(username='umlautUser', first_name="LastNameAsUTF8" , last_name=(b'\xC3\xB6\xC3\xA4\xC3\xBC').decode('utf-8'), email='user@praktomat.local', password='demü', is_staff=False, is_superuser=False)
        cls.umlautStudent.mat_number = 424242
        cls.umlautStudent.save()
        import datetime
        cls.umlautTask = Task.objects.create(title="German Umlauts äöü",description="Fußball is soccer. German umlauts are äöü",publication_date=datetime.date.today(),submission_date=datetime.date.today())
        cls.umlautTask.save()


    def setUp(self):
        from os.path import dirname, join
        self.client.login(username='trainer', password='demo')
        self.task = list(Task.objects.order_by('id').values())[-1]

        path = join(dirname(__file__), 'umlautstest.zip')
        with open(path, 'rb') as f:
            response = self.client.post(reverse('solution_list', args=[self.task['id']]), data={
                                'solutionfile_set-INITIAL_FORMS': '0',
                                'solutionfile_set-TOTAL_FORMS': '3',
                                'solutionfile_set-0-file': f
                            }, follow=True)
            self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.site = AdminSite()
        self.client.login(username='trainer', password='demo')


    def test_SolutionAdmin_ListView_shows_Umlauts(self):
        app_label = "solutions"
        model_name = "solution"
        response = self.client.get(reverse('admin:%s_%s_changelist' %(app_label, model_name)))
        self.assertEqual(response.status_code, 200, msg="Admin site : solutions solution : Status was %s != 200 : while forward lookup via URL" % response.status_code)
        self.assertNotIn("Internal Server Error".encode("utf-8"),response.content, msg="Admin site : solutions solution : shows \"Internal Server Error\"")

    def test_SolutionAdmin_ChangeView_shows_Umlauts(self):
        all_solutions = list(Solution.objects.order_by('id').values())
        app_label = "solutions"
        model_name = "solution"
        response = self.client.get('/admin/%s/%s/%s/change/'%(app_label,model_name,all_solutions[-1]['id']))
        self.assertEqual(response.status_code, 200, msg="Admin site : solutions solution : Status was %s != 200 : while forward lookup via URL" % response.status_code)
        self.assertNotIn("Internal Server Error".encode("utf-8"),response.content, msg="Admin site : solutions solution : change : shows \"Internal Server Error\"")


    def test_SolutionAdmin_UserView_shows_Umlauts(self):
        all_solutions = list(Solution.objects.order_by('id').values())
        app_label = "solutions"
        model_name = "solution"
        response = self.client.get(reverse('solution_detail_full', args=[all_solutions[-1]['id']]))
        self.assertEqual(response.status_code, 200, msg="Admin site : solutions solution : Status was %s != 200 : while forward lookup via URL" % response.status_code)
        self.assertIn("Fußballspieler".encode("utf-8"), response.content, msg="Admin site : solutions solution : user view : does not contain the right solution file \"Fußballspieler.java\"")
        self.assertIn("just have some utf-8 coded german umlauts äüö".encode("utf-8"), response.content, msg="Admin site : solutions solution : user view : does not contain the right solution file \"Fußballspieler.java\" having german umlauts in java line comment")
        self.assertNotIn("Internal Server Error".encode("utf-8"),response.content, msg="Admin site : solutions solution : user view : shows \"Internal Server Error\"")
