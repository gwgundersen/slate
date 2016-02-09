"""Unit tests for verifying a new user can be created with default categories.
"""

import unittest

from selenium import webdriver
from selenium.webdriver.support.select import Select

from utils import delete_user, login_user, register_user, SLATE_URL


class TestCreatingNewUser(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_new_user_categories(self):
        register_user(self.browser)
        login_user(self.browser)
        select = Select(
            self.browser.find_element_by_xpath('//select[@name="category_id"]')
        )
        default_categories = ['(category)',
                              'alcohol',
                              'food (in)',
                              'food (out)',
                              'transportation',
                              'rent/mortgage',
                              'bills',
                              'miscellaneous',
                              'household',
                              'travel/vacation',
                              'entertainment',
                              'medical',
                              'clothing',
                              'savings']
        for option in select.options:
            self.assertTrue(option.text.lower() in default_categories)
        delete_user(self.browser)

    def test_no_user_categories(self):
        self.browser.get(SLATE_URL)
        select = Select(
            self.browser.find_element_by_xpath('//select[@name="category_id"]')
        )
        self.assertTrue(len(select.options) == 1)

    def tearDown(self):
        self.browser.quit()
