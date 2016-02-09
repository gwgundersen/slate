"""Unit tests for verifying that an expense can be edited correctly.
"""

import unittest

from selenium import webdriver

from utils import add_expense, exists_by_xpath, login_user, delete_user, register_user
from config import SLATE_URL


class TestEditingExpense(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        register_user(self.browser)
        login_user(self.browser)

    def test_editing_expense(self):
        add_expense(self.browser, 7.50, 'Food (out)', 'Burrito')
        self.browser.get('%s/expenses' % SLATE_URL)
        self.browser.find_element_by_xpath('//input[@value="Edit"][1]')\
            .click()
        cost_input = self.browser\
            .find_element_by_xpath('//input[@name="cost"]')
        cost_input.clear()
        cost_input.send_keys(8.00)
        self.browser.find_element_by_xpath('//button[text()="Edit"]').click()
        td = self.browser.find_element_by_xpath('//table//tbody//td[1]')
        self.assertTrue(float(td.text), 8.00)

    def test_cancelling_edit(self):
        add_expense(self.browser, 7.50, 'Food (out)', 'Burrito')
        self.browser.get('%s/expenses' % SLATE_URL)
        self.browser.find_element_by_xpath('//input[@value="Edit"][1]')\
            .click()
        self.browser.find_element_by_xpath('//button[text()="Cancel"]')\
            .click()
        td = self.browser.find_element_by_xpath('//table//tbody//td[1]')
        self.assertTrue(float(td.text), 7.50)

    def test_deleting_expense(self):
        add_expense(self.browser, 9.00, 'Food (out)', 'Burrito')
        self.browser.get('%s/expenses' % SLATE_URL)
        self.browser.find_element_by_xpath('//input[@value="Edit"][1]')\
            .click()
        self.browser.find_element_by_xpath('//input[@value="Delete"]').click()
        alert = self.browser.switch_to_alert()
        alert.accept()
        self.assertTrue(
            not exists_by_xpath(self.browser, '//td[text()="9.00"]')
        )

    def tearDown(self):
        delete_user(self.browser)
        self.browser.quit()
