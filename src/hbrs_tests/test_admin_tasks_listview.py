# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from django.contrib.admin.sites import AdminSite

from accounts.models import User
from tasks.models import Task
from tasks.admin import TaskAdmin

class ModelTaskAdminTests(TestCase):

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
        self.site = AdminSite()
        self.client.login(username='trainer', password='demo')


    def test_TaskAdmin_ListView_shows_Umlauts(self):
        all_tasks = list(Task.objects.order_by('id').values())
        self.assertEqual(all_tasks[-1]['title'],"German Umlauts äöü")
        self.assertEqual(all_tasks[-1]['description'],"Fußball is soccer. German umlauts are äöü")
        # ö , ä , ü = 0xC3 0xB6 , 0xC3 0xA4 , 0xC3 0xBC : letters coded in UTF8
        self.assertEqual(all_tasks[-1]['title'].encode('utf-8'),b"German Umlauts \xC3\xA4\xC3\xB6\xC3\xBC")
        app_label = "tasks"
        model_name = "task"
        response = self.client.get(reverse('admin:%s_%s_changelist' %(app_label, model_name)))
        self.assertNotIn("Internal Server Error".encode("utf-8"),response.content, msg="Admin site : tasks task : shows \"Internal Server Error\"")
        self.assertIn("äöü".encode("utf-8"), response.content, msg="Admin site : tasks task : do not show task with german umlauts in title")


    def test_TaskAdmin_ChangeView_shows_Umlauts(self):
        all_tasks = list(Task.objects.order_by('id').values())
        self.assertEqual(all_tasks[-1]['title'],"German Umlauts äöü")
        self.assertEqual(all_tasks[-1]['description'],"Fußball is soccer. German umlauts are äöü")
        # ö , ä , ü = 0xC3 0xB6 , 0xC3 0xA4 , 0xC3 0xBC : Buchstaben als UTF8-codiert
        self.assertEqual(all_tasks[-1]['title'].encode('utf-8'),b"German Umlauts \xC3\xA4\xC3\xB6\xC3\xBC")
        app_label = "tasks"
        model_name = "task"
        response = self.client.get('/admin/%s/%s/%s/change/'%(app_label,model_name,all_tasks[-1]['id']))
        self.assertEqual(response.status_code, 200, msg="Admin site : tasks task : Status was %s != 200 : while forward lookup via URL" % response.status_code)
        self.assertNotIn("Internal Server Error".encode("utf-8"),response.content, msg="Admin site : tasks task : change : shows \"Internal Server Error\"")
        self.assertIn("äöü".encode("utf-8"), response.content, msg="Admin site : tasks task : change : do not show task with german umlauts in title")
