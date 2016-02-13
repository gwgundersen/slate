"""Unit tests for verifying a new category can be created.
"""

import unittest

from selenium import webdriver
from selenium.webdriver.support.select import Select

from utils import delete_user, register_user, get_flashed_message, SLATE_URL, \
    exists_by_xpath, add_expense


class TestEditingCategory(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        register_user(self.browser)
        self.browser.get('%s/account/settings' % SLATE_URL)

    def test_edit_category(self):
        self.browser.find_element_by_xpath('//a[text()="Edit"][1]').click()
        cost_input = self.browser\
            .find_element_by_xpath('//input[@name="category_name"]')
        cost_input.clear()
        cost_input.send_keys('edited test category')
        self.browser.find_element_by_xpath('//button[text()="Edit"]').click()
        self.assertTrue(exists_by_xpath(self.browser, '//tr[1]//td[text()="Edited test category"]'))

    def test_cancelling_edit(self):
        self.browser.find_element_by_xpath('//tr[1]//a[text()="Edit"]').click()
        self.browser.find_element_by_xpath('//a[text()="Cancel"]').click()
        self.assertTrue(exists_by_xpath(self.browser, '//tr[1]//td[text()="Alcohol"]'))

    def test_deleting_expense(self):
        self.browser.get(SLATE_URL)
        # We want to verify that this expense is deleted.
        add_expense(self.browser, 7.50, 'Food (out)', 'Burrito')
        self.browser.get('%s/account/settings' % SLATE_URL)
        self.browser.find_element_by_xpath('//tr//td[text()="Food (out)"]/..//a[text()="Edit"]').click()
        self.browser.find_element_by_xpath('//input[@value="Delete"]').click()
        alert = self.browser.switch_to_alert()
        alert.accept()
        self.browser.get(SLATE_URL)
        select = Select(
            self.browser.find_element_by_xpath('//select[@name="category_id"]')
        )
        for option in select.options:
            self.assertTrue(option.text != 'Food (out)')
        self.browser.get('%s/expenses' % SLATE_URL)
        self.assertFalse(
            exists_by_xpath(self.browser, '//td[text()="Food (out)"]')
        )

    def tearDown(self):
        delete_user(self.browser)
        self.browser.quit()
