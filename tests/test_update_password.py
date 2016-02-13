"""Unit tests for verifying a user can update their password.
"""

import unittest

from selenium import webdriver

from utils import delete_user, get_flashed_message, register_user, \
    update_password, MOCK_PW


class TestUpdatePassword(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        register_user(self.browser)

    def test_old_password_incorrect_error(self):
        update_password(self.browser, 'bar', 'foo', 'fo0')
        message = get_flashed_message(self.browser)
        self.assertEqual(message, 'Old password is incorrect.')

    def test_passwords_do_not_match_error(self):
        update_password(self.browser, MOCK_PW, 'foo', 'fo0')
        message = get_flashed_message(self.browser)
        self.assertEqual(message, 'Passwords do not match.')

    def test_password_is_required_error(self):
        update_password(self.browser, MOCK_PW, '', '')
        message = get_flashed_message(self.browser)
        self.assertEqual(message, 'Password is required.')

    def test_password_has_not_changed_error(self):
        update_password(self.browser, MOCK_PW, MOCK_PW, MOCK_PW)
        message = get_flashed_message(self.browser)
        self.assertEqual(message, 'Password has not changed.')

    def tearDown(self):
        delete_user(self.browser)
        self.browser.quit()
