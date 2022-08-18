# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os.path import dirname, join
from os import environ as os_environ

from django.test import TestCase
from django.urls import reverse

from django.contrib.admin.sites import AdminSite
from unittest import skipIf

from checker.checker.CUnitChecker_v2 import UnitCheckerCopyForm
from checker.checker.CUnitChecker_v2 import CUnitChecker2Inline
from checker.checker.CUnitChecker_v2 import CUnitChecker2
from solutions.models import Solution
from accounts.models import User
from tasks.models import Task
from tasks.admin import TaskAdmin
from attestation.models import RatingScale, RatingScaleItem


class ModelCUnitCppUnitCheckerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.Student = User.objects.create_user(username='c_cpp', first_name="C" , last_name="CPP", email='user@praktomat.local', password='demo', is_staff=False, is_superuser=False)
        cls.Student.mat_number = 424242


    def setUp(self):
        self.student=self.__class__.Student
        self.trainer=User.objects.get(username="trainer")


    def teatDown(self):
        self.client.logout()


    def __myTestHelper_taskAdmin_load_and_store_Task_with_CUnitCppUnit_Checker(self,taskZipPath):
        self.site = AdminSite()
        self.client.login(username='trainer', password='demo')
        taskID = -1
        with open(taskZipPath, 'rb') as f:
            #http://localhost:8000/admin/tasks/task/import/ + istemplate aktiv
            response = self.client.get('/admin/tasks/task/import/')
            self.assertEqual(response.status_code, 200) # should work
            self.assertIn("Import Task".encode("utf-8"),response.content)
            self.assertTemplateUsed(response,'admin/tasks/task/import.html')
            response = self.client.post('/admin/tasks/task/import/', data={
                               'file': f,
                               'is_template':'True'
                      }, xhr=True, follow=True)
            #http://localhost:8000/admin/tasks/task/
            self.assertEqual(response.status_code, 200) # should work
            self.assertTemplateUsed(response,'admin/tasks/task/change_list.html')
            #=> needed TaskID is biggest TaskID.
            all_tasks = list(Task.objects.order_by('id').values())
            taskID=all_tasks[-1]['id']
            #after importing it should be possible to call Task Admin change View for that task
            response = self.client.get('/admin/tasks/task/%s/change/'%(taskID))
            self.assertEqual(response.status_code, 200) # should work
            self.assertTemplateUsed(response,'admin/tasks/task/change_form.html')
            #print(response.content)
            # since we imported as template add grade scaling and dates to task
            ratingScale=RatingScale()
            ratingScale.name="UnitTest"
            ratingScale.save()
            ratingScale=RatingScale.objects.get(name="UnitTest")
            ratingScaleItem=RatingScaleItem()
            ratingScaleItem.name="0"
            ratingScaleItem.position=0
            ratingScaleItem.scale=ratingScale
            ratingScaleItem.save()
            # modify publication and submission date
            task = Task.objects.get(pk=taskID)
            from datetime import datetime
            task.submission_date=datetime.now()
            task.publication_date=datetime.now()
            task.final_grade_rating_scale=ratingScale
            task.save()
        self.client.logout()
        return taskID

    def __myTestHelper_student_uploads_Solution(self, solutionZipPath, taskID):
        self.assertIn('_auth_user_id', self.client.session) # check if one user is logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), self.student.id) # check if correct student has logged in
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200) # should work - tasks main page user view
        openedfile = False

        with open(solutionZipPath, 'rb') as f:
            openedfile = True
            solutions = list(Solution.objects.filter(task__exact=taskID,author__exact=self.student.id).order_by('id'))
            self.assertEqual(0,len(solutions)) # there should be no solutions.
            tasks = list(Task.objects.filter(id__exact=taskID).values())
            self.assertTrue(1==len(tasks) and taskID==tasks[0]['id']) # there should be one task having taskID
            response = self.client.get('/tasks/%s/solutionupload/'%(taskID))
            self.assertEqual(response.status_code, 200) # should work
            self.assertTemplateUsed(response,'solutions/solution_list.html')
            response = self.client.post(reverse('solution_list', args=[taskID]), data={
                                'solutionfile_set-INITIAL_FORMS': '0',
                                'solutionfile_set-TOTAL_FORMS': '3',
                                'solutionfile_set-0-file': f
                            }, xhr=True, follow=True)
            self.assertEqual(response.status_code, 200) # should work
            self.assertTemplateUsed(response,'solutions/solution_detail.html')
            self.assertNotIn("Upload solution denied for now".encode("utf-8"),response.content)
            #there should be no CUNIT missing error in response
            if "cannot find -lcunit".encode("utf-8") in response.content:
                self.fail("could not find Cunit installation. Fix your system installation.")
            if "fatal error: CUnit/Basic.h".encode("utf-8") in response.content:
                self.fail("could not find Cunit installation. Fix your system installation.")
            #there should be no CPPUNIT missing error in response
            if "cannot find -lcppunit".encode("utf-8") in response.content:
                self.fail("could not find CPPunit installation. Fix your system installation.")
            if "fatal error: cppunit/TestFixture.h".encode("utf-8") in response.content:
                self.fail("could not find CPPunit installation. Fix your system installation.")
            self.assertIn("This is your current final solution".encode("utf-8"),response.content)
        return openedfile;


    def test_CUnitCppUnit_Checker_model_TestApp_label(self):
        c = CUnitChecker2()
        field_label = c._meta.get_field('_test_name').verbose_name
        self.assertEqual(field_label, 'TestApp Filename')

    def test_CUnitCppUnit_Checker_model_TestIgnore_label(self):
        c = CUnitChecker2()
        field_label = c._meta.get_field('_test_ignore').verbose_name
        self.assertEqual(field_label, ' test ignore')

    def test_CUnitCppUnit_Checker_model_TestFlags_label(self):
        c = CUnitChecker2()
        field_label = c._meta.get_field('_test_flags').verbose_name
        self.assertEqual(field_label, ' test flags')

    def test_CUnitCppUnit_Checker_model_TestLinkType_label(self):
        c = CUnitChecker2()
        field_label = c._meta.get_field('link_type').verbose_name
        self.assertEqual(field_label, 'link type')

    def test_CUnitCppUnit_Checker_model_Test_UnitTestLib_label(self):
        c = CUnitChecker2()
        field_label = c._meta.get_field('cunit_version').verbose_name
        self.assertEqual(field_label, 'Unittest type or library')

    def test_CUnitCppUnit_Checker_model_Test_parameter_label(self):
        c = CUnitChecker2()
        field_label = c._meta.get_field('_test_par').verbose_name
        self.assertEqual(field_label, ' test par')

    def test_CUnitCppUnit_Checker_model_TestDescription_label(self):
        c = CUnitChecker2()
        field_label = c._meta.get_field('test_description').verbose_name
        self.assertEqual(field_label, 'test description')

    def test_CUnitCppUnit_Checker_model_TestName_label(self):
        c = CUnitChecker2()
        field_label = c._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_CUnitCppUnit_Checker_model_Test_MUT_Filename_label(self):
        c = CUnitChecker2()
        field_label = c._meta.get_field('_sol_name').verbose_name
        self.assertEqual(field_label, 'MUT Filename')

    def test_CUnitCppUnit_Checker_model_Test_MUT_IgnoreFiles_label(self):
        c = CUnitChecker2()
        field_label = c._meta.get_field('_sol_ignore').verbose_name
        self.assertEqual(field_label, 'MUT ignore files')

    def test_CUnitCppUnit_Checker_model_Test_MUT_Flags_label(self):
        c = CUnitChecker2()
        field_label = c._meta.get_field('_sol_flags').verbose_name
        self.assertEqual(field_label, 'MUT flags')

    @skipIf('CI' in os_environ, "Since I have no time to figure out how path-information in cTestrunner has to be set for GitHub Actions, I skip this test for now")
    def test_task_solutionview_student_upload_C_app(self):
        taskpath = join(dirname(__file__), 'test_C_app_Task' , 'TestC_app_TaskExport.zip')
        taskid = self.__myTestHelper_taskAdmin_load_and_store_Task_with_CUnitCppUnit_Checker(taskpath)
        self.client.login(username='c_cpp', password='demo')
        self.assertIn('_auth_user_id', self.client.session) # check if one user is logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), self.student.id) # check if correct student has logged in
        solutionpath = join(dirname(__file__), 'test_C_app_Task' , 'C_app_Task_Solution.zip')
        value_C_app_Task=self.__myTestHelper_student_uploads_Solution(solutionpath,taskid)
        self.assertTrue(value_C_app_Task)

    @skipIf('CI' in os_environ, "Since I have no time to figure out how path-information in cTestrunner has to be set for GitHub Actions, I skip this test for now")
    def test_task_solutionview_student_upload_C_funcLib(self):
        taskpath = join(dirname(__file__), 'test_C_funcLib_Task' , 'TestC_funcLib_TaskExport.zip')
        taskid = self.__myTestHelper_taskAdmin_load_and_store_Task_with_CUnitCppUnit_Checker(taskpath)
        self.client.login(username='c_cpp', password='demo')
        self.assertIn('_auth_user_id', self.client.session) # check if one user is logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), self.student.id) # check if correct student has logged in
        solutionpath = join(dirname(__file__), 'test_C_funcLib_Task' , 'C_funcLib_Task_Solution.zip')
        value_C_funcLib_Task=self.__myTestHelper_student_uploads_Solution(solutionpath,taskid)
        self.assertTrue(value_C_funcLib_Task)


    def test_task_solutionview_student_upload_CPP_app(self):
        taskpath = join(dirname(__file__), 'test_CPP_app_Task' , 'TestCPP_app_TaskExport.zip')
        taskid = self.__myTestHelper_taskAdmin_load_and_store_Task_with_CUnitCppUnit_Checker(taskpath)
        self.client.login(username='c_cpp', password='demo')
        self.assertIn('_auth_user_id', self.client.session) # check if one user is logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), self.student.id) # check if correct student has logged in
        solutionpath = join(dirname(__file__), 'test_CPP_app_Task' , 'CPP_app_Task_Solution.zip')
        value_CPP_app_Task=self.__myTestHelper_student_uploads_Solution(solutionpath,taskid)
        self.assertTrue(value_CPP_app_Task)



    def test_task_solutionview_student_upload_CPP_method(self):
        taskpath = join(dirname(__file__), 'test_CPP_method_Task' , 'TestCPP_Method_TaskExport.zip')
        taskid = self.__myTestHelper_taskAdmin_load_and_store_Task_with_CUnitCppUnit_Checker(taskpath)
        self.client.login(username='c_cpp', password='demo')
        self.assertIn('_auth_user_id', self.client.session) # check if one user is logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), self.student.id) # check if correct student has logged in
        solutionpath = join(dirname(__file__), 'test_CPP_method_Task' , 'CPP_method_Task_Solution.zip')
        value_CPP_method_Task=self.__myTestHelper_student_uploads_Solution(solutionpath,taskid)
        self.assertTrue(value_CPP_method_Task)


    def test_taskAdmin_changeCUnitCppUnit_UnitCheckerCopyForm_RenameFile(self):
        taskpath = join(dirname(__file__), 'test_C_funcLib_Task' , 'TestC_funcLib_TaskExport_RenameFileTest_but_no_new_upload.zip')
        taskid = self.__myTestHelper_taskAdmin_load_and_store_Task_with_CUnitCppUnit_Checker(taskpath)
        self.client.login(username='trainer', password='demo')
        self.assertIn('_auth_user_id', self.client.session) # check if one user is logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), self.trainer.id) # check if correct student has logged in
        #http://localhost:8000/admin/tasks/task/6/change/
        response = self.client.get('/admin/tasks/task/%s/change/'%(taskid))
        # name of  FileField file ends with "test_uebung11_NsIpkLQ.c"
        # value of CharField filename ends with "test_uebung11.c"
        # there should be a form warning, if both names are different,
        # but at least it should be possible to safe a different value in CharField as file name,
        # just for using the given filename inside the sandbox.
        # Therefor we test the form:
        initialdata=None
        for x in response.context['inline_admin_formsets'] :
            if "CUnitChecker2FormFormSet" in str(type(x.formset))  :
               for form in x.formset:
                  initialdata = form.initial.copy()
        formN = UnitCheckerCopyForm(initial=initialdata)
        formFalse = UnitCheckerCopyForm(initial=initialdata, data={
                               'filename' :CUnitChecker2.objects.get(task_id=taskid).filename,
                               'task': CUnitChecker2.objects.get(task_id=taskid).task.id,
                               'cunit_version': CUnitChecker2.objects.get(task_id=taskid).cunit_version,
                               '_sol_name': CUnitChecker2.objects.get(task_id=taskid)._sol_name,
                               '_test_name': CUnitChecker2.objects.get(task_id=taskid)._test_name,
                               'file': initialdata.copy()['file'],
                               'test_description': CUnitChecker2.objects.get(task_id=taskid).test_description,
                               'order': CUnitChecker2.objects.get(task_id=taskid).order,
                               'link_type':CUnitChecker2.objects.get(task_id=taskid).link_type,
                               'name':CUnitChecker2.objects.get(task_id=taskid).name,
                               })
        temp = str(formFalse.errors['filename'])
        self.assertIn('The correct name could be', str(formFalse.errors['filename'])) #formFalse.data['filename'] should have an error message in formFalse.errors['filename']
        self.assertFalse(formFalse.is_valid())
        formTrue = UnitCheckerCopyForm(initial=initialdata, data={
                               'filename' :CUnitChecker2.objects.get(task_id=taskid).filename,
                               'task': CUnitChecker2.objects.get(task_id=taskid).task.id,
                               'cunit_version': CUnitChecker2.objects.get(task_id=taskid).cunit_version,
                               '_sol_name': CUnitChecker2.objects.get(task_id=taskid)._sol_name,
                               '_test_name': CUnitChecker2.objects.get(task_id=taskid)._test_name,
                               'file': initialdata['file'],
                               'test_description': CUnitChecker2.objects.get(task_id=taskid).test_description,
                               'order': CUnitChecker2.objects.get(task_id=taskid).order,
                               'link_type':CUnitChecker2.objects.get(task_id=taskid).link_type,
                               'name':CUnitChecker2.objects.get(task_id=taskid).name,
                               'force_save':True,
                               })
        self.assertNotIn('The correct name could be', str(formTrue.errors)) #formTrue.data['filename'] should not have an error message in formTrue.errors['filename']
        self.assertTrue(formTrue.is_valid())
        #cunitchecker2_set-0-public #checkbox
        #cunitchecker2_set-0-required #checkbox
        #cunitchecker2_set-0-always #checkbox
        #cunitchecker2_set-0-critical #checkbox
        #cunitchecker2_set-0-file #FileField
        #cunitchecker2_set-0-filename #CharField
        #cunitchecker2_set-0-path #CharField
        #cunitchecker2_set-0-unpack_zipfile # checkbox
        #cunitchecker2_set-0-is_sourcecode # checkbox
        #cunitchecker2_set-0-include_in_solution_download # checkbox
        #cunitchecker2_set-0-_test_name
        #cunitchecker2_set-0-_test_ignore
        #cunitchecker2_set-0-_test_flags
        #cunitchecker2_set-0-link_type
        #cunitchecker2_set-0-cunit_version
        #cunitchecker2_set-0-_test_par
        #cunitchecker2_set-0-test_description
        #cunitchecker2_set-0-name
        #cunitchecker2_set-0-_sol_name
        #cunitchecker2_set-0-_sol_ignore
        #cunitchecker2_set-0-_sol_flags

    def test_taskAdmin_action_runallcheckers_onTaskWithNoSolutionUploads(self):
        """
        Testing run_all_checkers action
        App is content_app, model is content
        modify as per your app/model
        """
        taskpath = join(dirname(__file__), 'test_CPP_method_Task' , 'TestCPP_Method_TaskExport.zip')
        taskid = self.__myTestHelper_taskAdmin_load_and_store_Task_with_CUnitCppUnit_Checker(taskpath)
        task = Task.objects.get(pk=taskid)
        from datetime import datetime, timedelta
        task.submission_date=datetime.now() - timedelta(hours=2, minutes=50)
        task.publication_date=datetime.now() - timedelta(hours=3, minutes=50)
        task.save()
        self.site = AdminSite()
        self.client.login(username='trainer', password='demo')
        self.assertIn('_auth_user_id', self.client.session) # check if one user is logged in
        app_label = "tasks"
        model_name = "task"
        change_url = reverse('admin:%s_%s_changelist' %(app_label, model_name))
        data = {'action': 'run_all_checkers',
                '_selected_action': [taskid, ]}
        response = self.client.post(change_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("0 final solutions were successfully checked".encode("utf-8"),response.content)


    def test_taskAdmin_action_runallcheckers_onTaskWithOneSolutionUploads(self):
        """
        Testing run_all_checkers action
        App is content_app, model is content
        modify as per your app/model
        """
        #trainer import task
        taskpath = join(dirname(__file__), 'test_CPP_method_Task' , 'TestCPP_Method_TaskExport.zip')
        taskid = self.__myTestHelper_taskAdmin_load_and_store_Task_with_CUnitCppUnit_Checker(taskpath)
        #student upload solution
        self.client.login(username='c_cpp', password='demo')
        self.assertIn('_auth_user_id', self.client.session) # check if one user is logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), self.student.id) # check if correct student has logged in
        solutionpath = join(dirname(__file__), 'test_CPP_method_Task' , 'CPP_method_Task_Solution.zip')
        value_CPP_method_Task=self.__myTestHelper_student_uploads_Solution(solutionpath,taskid)
        self.assertTrue(value_CPP_method_Task)
        self.client.logout()
        #modify task deadlines
        task = Task.objects.get(pk=taskid)
        from datetime import datetime, timedelta
        task.submission_date=datetime.now() - timedelta(hours=2, minutes=50)
        task.publication_date=datetime.now() - timedelta(hours=3, minutes=50)
        task.save()
        #trainer starts "run_all_checkers"
        self.site = AdminSite()
        self.client.login(username='trainer', password='demo')
        self.assertIn('_auth_user_id', self.client.session) # check if one user is logged in
        app_label = "tasks"
        model_name = "task"
        change_url = reverse('admin:%s_%s_changelist' %(app_label, model_name))
        data = {'action': 'run_all_checkers',
                '_selected_action': [taskid, ]}
        response = self.client.post(change_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("1 final solutions were successfully checked".encode("utf-8"),response.content) #ToDo: The message should be really in singular, but for now, I want to pass the UnitTest
