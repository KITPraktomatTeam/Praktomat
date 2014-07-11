from utilities.TestSuite import TestCase, SeleniumTestCase
from accounts.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from StringIO import StringIO


class TestViewsSelenium(SeleniumTestCase):
    def test_login(self):
        self.loginAsUser()
        self.assertIn("/tasks/", self.selenium.current_url)
        user_tools = self.selenium.find_element_by_id('user-tools')
        self.assertIn("Welcome, user", user_tools.text)


class TestViews(TestCase):
    def setUp(self):
        self.client.login(username='trainer', password='demo')
        self.testgroup = Group(name = 'test')
        self.testgroup.save()

    def test_get_testgroup(self):
        response = self.client.get(reverse('admin:auth_group_change', args=[self.testgroup.id]))
        self.failUnlessEqual(response.status_code, 200)

    def test_testgroup_empty(self):
        self.failUnlessEqual(set(self.testgroup.user_set.all()), set())

    def test_testgroup_add_user(self):
        # mostly to test the testing
        user = User.objects.get(username = 'user')
        user.groups.add(self.testgroup)
        user.save()
        self.failUnlessEqual(set( u.mat_number for u in User.objects.filter(groups = self.testgroup)),
                             set( u.mat_number for u in [user]))

    def test_testgroup_add_to_group(self):
        user = User.objects.get(username = 'user')

        user2 = User.objects.create_user('user2', 'user@praktomat.com', 'demo')
        user2.mat_number = 22222
        user2.groups.add(self.testgroup)
        user2.save()

        f = StringIO("11111\n33333")
        f.name="foo.txt"
        response = self.client.post(
            reverse('admin:import_matriculation_list', args=[self.testgroup.id]),
            { 'mat_number_file': f,
              'remove_others' : False,
              'create_users': False},
            follow=True)
        self.assertContains(response, "1 users added to group test, 0 removed, 0 already in group. 0 new users created.")
        self.failUnlessEqual(set( u.mat_number for u in User.objects.filter(groups = self.testgroup)),
                             set( u.mat_number for u in [user,user2]))

    def test_testgroup_set_group(self):
        user = User.objects.get(username = 'user')

        user2 = User.objects.create_user('user2', 'user@praktomat.com', 'demo')
        user2.mat_number = 22222
        user2.groups.add(self.testgroup)
        user2.save()

        f = StringIO("11111\n33333")
        f.name="foo.txt"
        response = self.client.post(
            reverse('admin:import_matriculation_list', args=[self.testgroup.id]),
            { 'mat_number_file': f,
              'remove_others' : True,
              'create_users': False},
            follow=True)
        self.assertContains(response, "1 users added to group test, 1 removed, 0 already in group. 0 new users created.")
        self.failUnlessEqual(set( u.mat_number for u in User.objects.filter(groups = self.testgroup)),
                             set( u.mat_number for u in [user]))

    def test_testgroup_set_group(self):
        # mostly to test the testing
        user = User.objects.get(username = 'user')

        user2 = User.objects.create_user('user2', 'user@praktomat.com', 'demo')
        user2.mat_number = 22222
        user2.groups.add(self.testgroup)
        user2.save()

        f = StringIO("11111\n33333")
        f.name="foo.txt"
        response = self.client.post(
            reverse('admin:import_matriculation_list', args=[self.testgroup.id]),
            { 'mat_number_file': f,
              'remove_others' : True,
              'create_users': True},
            follow=True)
        self.assertContains(response, "2 users added to group test, 1 removed, 0 already in group. 1 new users created.")

        user3 = User.objects.get(mat_number = 33333)

        self.failUnlessEqual(set( u.mat_number for u in User.objects.filter(groups = self.testgroup)),
                             set( u.mat_number for u in [user,user3]))

