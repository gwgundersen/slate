"""Unit tests for verifying a new user can be created with default categories.
"""

import unittest

from selenium import webdriver
from selenium.webdriver.support.select import Select

from utils import delete_user, register_user, SLATE_URL, DEFAULT_CATEGORIES, \
    get_flashed_message, wait_until, login_user


class TestCreatingNewUser(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_new_user_categories(self):
        register_user(self.browser)
        elem = wait_until(self.browser, '//select[@name="category_id"]')
        select = Select(elem)
        for option in select.options:
            if option.text == '(category)':
                self.assertTrue(option.text not in DEFAULT_CATEGORIES)
            else:
                self.assertTrue(option.text.lower() in DEFAULT_CATEGORIES)
        delete_user(self.browser)

    def test_alphanumeric_username(self):
        register_user(self.browser, username='@@@', should_fail=True)
        message = get_flashed_message(self.browser)
        self.assertEqual(message, 'Username must be alphanumeric.')
        # No delete. User should not have been created.

    def test_user_exists_error(self):
        register_user(self.browser)
        # Force Selenium to wait until the new user has been created.
        get_flashed_message(self.browser)
        register_user(self.browser, should_fail=True)
        message = get_flashed_message(self.browser)
        self.assertEqual(message, 'Username already exists.')
        # Delete. First user would have been created.
        delete_user(self.browser)

    def test_different_passwords_error(self):
        register_user(self.browser, password1='foo', password2='fo0',
                      should_fail=True)
        message = get_flashed_message(self.browser)
        self.assertEqual(message, 'Passwords do not match.')
        # No delete. User should not have been created.

    def test_no_password_error(self):
        register_user(self.browser, password1='', password2='',
                      should_fail=True)
        message = get_flashed_message(self.browser)
        self.assertEqual(message, 'Password is required.')
        # No delete. User should not have been created.

    def test_success_message(self):
        register_user(self.browser)
        message = get_flashed_message(self.browser)
        self.assertEqual(message, 'Welcome to Slate!')
        delete_user(self.browser)

    def test_no_user_categories(self):
        self.browser.get(SLATE_URL)
        elem = wait_until(self.browser, '//select[@name="category_id"]')
        select = Select(elem)
        self.assertTrue(len(select.options) == 1)
        # No delete. User should not have been created.

    def tearDown(self):
        self.browser.quit()
