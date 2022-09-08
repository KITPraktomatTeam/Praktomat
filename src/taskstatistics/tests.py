# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

try:
    from django.urls import resolve
except ImportError:
    from django.core.urlresolvers import resolve


from django.http import HttpRequest
from django.template.loader import render_to_string

from django.db import migrations
from django.db import connection

from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

from taskstatistics.models import TasksStatistic
from taskstatistics.views import tasks_statistic
from taskstatistics.views import prepare_statistic_data
from taskstatistics.views import prepare_graphic_list
from taskstatistics.views import tasks_statistic_download

from solutions.models import Solution
from tasks.models import Task

from collections import OrderedDict

class TasksStatisticTest(TestCase):

    def get_table_description(self, table):
        with connection.cursor() as cursor:
           return connection.introspection.get_table_description(cursor, table)

    def assertTableOrViewExists(self, tableOrView):
        with connection.cursor() as cursor:
           self.assertIn(tableOrView, connection.introspection.table_names(cursor, include_views=True))

    def test_DBview_tasksstatistic_isavailable(self):
        #check if view with correct name as been created in database
        self.assertTableOrViewExists("dbview_tasksstatistic")
        #heuristic check about correct created view, that is checking if database view has a attribute with needed field name
        self.assertIn("up_whisker_upl_until_final_pass", str(self.get_table_description("dbview_tasksstatistic")))

    def test_Model_TasksStatistic_isavailable(self):
        v=TasksStatistic.objects.values()
        self.assertIn("QuerySet", str(v))

    def test_Foreignkey_Connection_works(self):
        ts = TasksStatistic.objects.get(pk=1)
        self.assertIsInstance(ts,TasksStatistic)
        t = ts.task
        self.assertIsInstance(t,Task)


    def test_Model_TasksStatistic_isUnmanaged(self):
        self.assertFalse(TasksStatistic._meta.managed, "TasksStatistic should be a not managed class since it use a database view.")

    def test_tasksstatistic_url_resolves_to_tasksstatistic_view(self):
        found = resolve('/tasks/statistic')
        self.assertEqual(found.func, tasks_statistic, "Update urls.py to make url resolveable.")

    def test_taskstatistic_returns_correct_html_title(self):
        request = HttpRequest()

        """Annotate a request object with a session"""
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        """Annotate a request object with a messages"""
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()


        response = tasks_statistic(request)
        self.assertContains(text="<!DOCTYPE html",response=response,html=False)
        self.assertContains(text="<html",response=response,html=False)
        self.assertTrue(response.content.strip().startswith(b'<!DOCTYPE html'), "No HTML Doctype has been defined at beginning.")
        self.assertIn(b'<h1>Task statistics</h1>', response.content, "Website has wrong h1 element, maybe its content is wrong, too.")
        self.assertTrue(response.content.strip().endswith(b'</html>'), "No valid HTML has been returned.")

    def remove_csrf_tag(self, text):
        """Remove csrf tag from TEXT"""
        import re
        return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)


    def test_taskstatistic_returns_correct_html(self):
        request = HttpRequest()

        """Annotate a request object with a session"""
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        """Annotate a request object with a messages"""
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        response = tasks_statistic(request)
        data_ , tasks_ = prepare_statistic_data()
        graphic_list_ = prepare_graphic_list(data_)
        context = {'data':data_ , 'graphics':graphic_list_ }
        expected_html = render_to_string('taskstatistics/overview.html',context,request=request)
        self.assertEqual(self.remove_csrf_tag(response.content.strip().decode('utf-8')),self.remove_csrf_tag(expected_html.strip()))

    def test_taskstatistic_uses_Template(self):
        self.client.login(username='trainer', password='demo')
        response = self.client.get('/tasks/statistic')
        self.assertTemplateUsed(response,'taskstatistics/overview.html')
        self.assertEqual(response.status_code, 200) # should work
        self.client.logout()

    def test_taskstatistic_returns_html_table_for_trainers(self):
        data_ , tasks_ = prepare_statistic_data()
        context = {'data':data_ }
        #print(context)
        html_output = render_to_string('taskstatistics/overview.html', context)
        #print(html_output)
        self.assertNotIn("<table" , html_output , "There shouldn't be a html table on statistic overview page for non trainers.")
        self.assertNotIn("median" , html_output )
        self.client.login(username='trainer', password='demo')
        responseC = self.client.get('/tasks/statistic')
        self.assertEqual(responseC.status_code, 200) # should work
        self.assertIn("<table".encode("utf-8"), responseC.content, "There should be a html table on statistic overview page for trainers.")
        self.client.logout()

    def test_column_order_as_basis_for_html_table(self):
        data_ , tasks_ = prepare_statistic_data()
        self.assertIs(type(data_), list)
        for f in data_:
            self.assertIs(type(f), OrderedDict)

    def test_tasksstatistic_url_resolves_to_tasksstatistic_download(self):
        found = resolve('/tasks/statistic/download')
        self.assertEqual(found.func, tasks_statistic_download, "Update urls.py to make url resolveable.")

    def test_taskstatistic_csv_download(self):
        data_ , tasks_ = prepare_statistic_data()
        context = {'data':data_ }
        html_output = render_to_string('taskstatistics/overview.html', context)
        self.assertNotIn("<a href=/tasks/statistic/download", html_output, "There should not be a download link on statistic overview page, without login as tutor, trainer or superuser")
        self.client.login(username='trainer', password='demo')
        responseC = self.client.get('/tasks/statistic')
        self.assertEqual(responseC.status_code, 200) # should work
        self.assertIn("<a href=/tasks/statistic/download".encode("utf-8"), responseC.content, "There should be a download link on statistic overview page")
        self.client.logout() # without login a statistic view should possible, if there are data.
        responseC = self.client.get('/tasks/statistic/download')
        self.assertEqual(responseC.status_code, 200) # should work
        request = HttpRequest()

        """Annotate a request object with a session"""
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        """Annotate a request object with a messages"""
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        response = tasks_statistic_download(request)

        self.assertEqual(self.remove_csrf_tag(responseC.content.strip().decode("utf-8")), self.remove_csrf_tag(response.content.strip().decode("utf-8")))
        self.client.logout()

    # ToDo: Think of integrating Whisker-Boxplot-Data for given Task on statistics View of attestation.
    # URL is like  tasks/1363/attestation/statistics
    # self.fail('Finish the test')
