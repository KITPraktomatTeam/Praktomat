# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from django.contrib.admin.sites import AdminSite

from accounts.models import User
from accounts.admin import UserAdmin

#Some of our users have non-ASCII based names, therefor we create such a user, and testing the admin interface

class ModelUserAdminTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # ö , ä , ü = 0xC3 0xB6 , 0xC3 0xA4 , 0xC3 0xBC : letters coded in UTF8
        cls.umlautStudent = User.objects.create_user(username='umlautUser', first_name="LastNameAsUTF8" , last_name=(b'\xC3\xB6\xC3\xA4\xC3\xBC').decode("utf-8"), email='user@praktomat.local', password='demü', is_staff=False, is_superuser=False)
        cls.umlautStudent.mat_number = 424242
        cls.umlautStudent.save()


    def setUp(self):
        self.site = AdminSite()
        self.client.login(username='trainer', password='demo')

    def test_UserAdmin_str(self):
        ua = UserAdmin(User, self.site)
        self.assertEqual(str(ua), 'accounts.UserAdmin')

    def test_UserAdminView_url_exists_at_desired_location(self):
        response = self.client.get('/admin/accounts/user/')
        self.assertEqual(response.status_code, 200, msg="Admin site : users user : Status was %s != 200 : while forward lookup via URL" % response.status_code)

    def test_view_url_accessible_by_name(self):
        url = reverse("admin:accounts_user_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, msg="Admin site : users user : Status was %s != 200 : while reverse lookup from function name" % response.status_code)

    def test_view_uses_correct_template(self):
        app_label = "accounts"
        model_name = "user"
        response = self.client.get(reverse('admin:%s_%s_changelist' %(app_label, model_name)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/accounts/user/change_list.html')

    def test_UserAdmin_ListView_shows_Umlauts(self):
        all_users = list(User.objects.values())
        self.assertEqual(all_users[-1]['username'],"umlautUser")
        self.assertEqual(all_users[-1]['last_name'],"öäü")
        self.assertEqual(all_users[-1]['last_name'].encode("utf-8"),b'\xC3\xB6\xC3\xA4\xC3\xBC')
        app_label = "accounts"
        model_name = "user"
        response = self.client.get(reverse('admin:%s_%s_changelist' %(app_label, model_name)))
        self.assertNotIn("Internal Server Error".encode("utf-8"),response.content, msg="Admin site : users user : shows \"Internal Server Error\"")
        self.assertIn("öäü".encode("utf-8"), response.content, msg="Admin site : users user : do not show user with german umlauts")

    def test_UserAdmin_ChangeView_shows_Umlauts(self):
        all_users = list(User.objects.order_by('id').values())
        self.assertEqual(all_users[-1]['username'],"umlautUser")
        self.assertEqual(all_users[-1]['last_name'],"öäü")
        self.assertEqual(all_users[-1]['last_name'].encode("utf-8"),b'\xC3\xB6\xC3\xA4\xC3\xBC')
        app_label = "accounts"
        model_name = "user"
        response = self.client.get('/admin/%s/%s/%s/change/'%(app_label,model_name,all_users[-1]['id']))
        self.assertEqual(response.status_code, 200, msg="Admin site : users user : Status was %s != 200 : while forward lookup via URL" % response.status_code)
        self.assertNotIn("Internal Server Error".encode("utf-8"),response.content, msg="Admin site : users user : change : shows \"Internal Server Error\"")
        self.assertIn("öäü".encode("utf-8"), response.content, msg="Admin site : users user : change : do not show user with german umlauts")
