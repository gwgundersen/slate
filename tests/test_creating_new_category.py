"""Unit tests for verifying a new category can be created.
"""

import unittest
import time

from selenium import webdriver

from utils import delete_user, register_user, get_flashed_message, SLATE_URL, \
    exists_by_xpath


class TestCreatingNewUser(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        register_user(self.browser)
        self.browser.get('%s/account/settings' % SLATE_URL)

    def test_create_new_category(self):
        input = self.browser.find_element_by_xpath('//input[@name="category_name"]')
        input.send_keys('new test category')
        self.browser.find_element_by_xpath('//input[@type="submit"]').click()
        # Notice that the user interface will capitalize the category.
        xpath = '//table//tr//td[text()="New test category"]'
        time.sleep(2)
        self.assertTrue(exists_by_xpath(self.browser, xpath))

    def test_existing_category_error(self):
        input = self.browser.find_element_by_xpath('//input[@name="category_name"]')
        input.send_keys('bills')
        self.browser.find_element_by_xpath('//input[@type="submit"]').click()
        message = get_flashed_message(self.browser)
        self.assertEqual(message, 'Category by that name already exists.')

    def tearDown(self):
        delete_user(self.browser)
        self.browser.quit()
