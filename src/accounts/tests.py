from utilities.TestSuite import TestCase, SeleniumTestCase

class TestViewsSelenium(SeleniumTestCase):
    def test_login(self):
        self.loginAsUser()
        self.assertIn("/tasks/", self.selenium.current_url)
        user_tools = self.selenium.find_element_by_id('user-tools')
        self.assertIn("Welcome, user", user_tools.text)



