"""Unit tests for verifying that an expense can be edited correctly.
"""

import unittest

from selenium import webdriver
from selenium.webdriver.support.select import Select

from utils import add_expense, delete_user, exists_by_xpath, register_user, \
    get_flashed_message, DEFAULT_CATEGORIES, SLATE_URL


class TestEditingExpense(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        register_user(self.browser)

    def test_editing_expense(self):
        add_expense(self.browser, '7.50', 'Food (out)', 'Burrito')
        self.browser.get('%s/expenses' % SLATE_URL)
        self.browser.find_element_by_xpath('//a[text()="Edit"][1]')\
            .click()
        cost_input = self.browser\
            .find_element_by_xpath('//input[@name="cost"]')
        cost_input.clear()
        cost_input.send_keys('8.00')
        self.browser.find_element_by_xpath('//button[text()="Edit"]').click()
        td = self.browser.find_element_by_xpath('//table//tbody//td[1]')
        self.assertTrue(float(td.text), '8.00')

    def test_cancelling_edit(self):
        add_expense(self.browser, '7.50', 'Food (out)', 'Burrito')
        self.browser.get('%s/expenses' % SLATE_URL)
        self.browser.find_element_by_xpath('//a[text()="Edit"][1]')\
            .click()
        self.browser.find_element_by_xpath('//a[text()="Cancel"]')\
            .click()
        td = self.browser.find_element_by_xpath('//table//tbody//td[1]')
        self.assertTrue(float(td.text), '7.50')

    def test_deleting_expense(self):
        add_expense(self.browser, '9.00', 'Food (out)', 'Burrito')
        self.browser.get('%s/expenses' % SLATE_URL)
        self.browser.find_element_by_xpath('//a[text()="Edit"][1]')\
            .click()
        self.browser.find_element_by_xpath('//input[@value="Delete"]').click()
        self.browser.switch_to.alert.accept()
        self.assertTrue(
            not exists_by_xpath(self.browser, '//td[text()="9.00"]')
        )

    def test_cost_validation(self):
        add_expense(self.browser, '7.50', 'Food (out)', 'Burrito')
        self.browser.get('%s/expenses' % SLATE_URL)
        self.browser.find_element_by_xpath('//a[text()="Edit"][1]')\
            .click()
        cost_input = self.browser\
            .find_element_by_xpath('//input[@name="cost"]')
        cost_input.clear()
        cost_input.send_keys('Eight dollars')
        self.browser.find_element_by_xpath('//button[text()="Edit"]').click()
        message = get_flashed_message(self.browser)
        self.assertEqual(message, 'Cost must be a number.')

    def test_comment_validation(self):
        add_expense(self.browser, '7.50', 'Food (out)', 'Burrito')
        self.browser.get('%s/expenses' % SLATE_URL)
        self.browser.find_element_by_xpath('//a[text()="Edit"][1]')\
            .click()
        comment_input = self.browser\
            .find_element_by_xpath('//input[@name="comment"]')
        comment_input.clear()
        comment_input.send_keys('')
        self.browser.find_element_by_xpath('//button[text()="Edit"]').click()
        message = get_flashed_message(self.browser)
        self.assertEqual(message, 'Comment is required.')

    def test_category_selection_and_options(self):
        add_expense(self.browser, '7.50', 'Food (out)', 'Burrito')
        self.browser.get('%s/expenses' % SLATE_URL)
        self.browser.find_element_by_xpath('//a[text()="Edit"][1]')\
            .click()
        select = Select(
            self.browser.find_element_by_xpath('//select[@name="category_id"]')
        )
        self.assertEqual(select.first_selected_option.text, 'Food (out)')
        self.assertTrue(len(select.options) == len(DEFAULT_CATEGORIES))

    def tearDown(self):
        delete_user(self.browser)
        self.browser.quit()
