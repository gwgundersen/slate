"""Unit tests for verifying login, logout, and registration.
"""

import unittest

from selenium import webdriver

from testutils import exists_by_xpath, login_user, logout_user
from config import SLATE_URL, MOCK_USER


class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('%s/login' % SLATE_URL)

    def test_login(self):
        login_user(self.browser)
        span = self.browser.find_element_by_xpath('//div[@id="header"]//span')
        self.assertEqual(span.text, MOCK_USER)
        self.assertTrue(
            exists_by_xpath(self.browser, '//button[text()="Logout"]')
        )
        self.assertTrue(
            exists_by_xpath(self.browser, '//a[text()="Account"]')
        )
        self.assertTrue(
            not exists_by_xpath(self.browser, '//a[text()="Login"]')
        )
        self.assertTrue(
            not exists_by_xpath(self.browser, '//a[text()="Register"]')
        )

    def test_logout(self):
        login_user(self.browser)
        logout_user(self.browser)
        span = self.browser.find_element_by_xpath('//div[@id="header"]//span')
        self.assertEqual(span.text, 'No user logged in.')
        self.assertTrue(
            not exists_by_xpath(self.browser, '//button[text()="Logout"]')
        )
        self.assertTrue(
            not exists_by_xpath(self.browser, '//a[text()="Account"]')
        )
        self.assertTrue(
            exists_by_xpath(self.browser, '//a[text()="Login"]')
        )
        self.assertTrue(
            exists_by_xpath(self.browser, '//a[text()="Register"]')
        )

    def tearDown(self):
        self.browser.quit()
