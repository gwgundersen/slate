"""Unit tests for verifying logging in and logging out. These utility methods
are sprinkled throughout the unit tests, so if they fail, nearly every test
should fail. That said, it's good to be explicit.
"""

import unittest

from selenium import webdriver

from utils import login_user, logout_user, register_user, delete_user


class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # register_use is tested explicitly in test_create_new_user.py
        register_user(self.browser)

    def test_login(self):
        login_user(self.browser)
        delete_user(self.browser)

    def test_logout(self):
        login_user(self.browser)
        logout_user(self.browser)
        login_user(self.browser)
        delete_user(self.browser)

    def tearDown(self):
        self.browser.quit()
