"""Unit tests for verifying that an expense can be added correctly. This is
the one pipeline we never want to break.
"""

import unittest

from selenium import webdriver

from utils import add_expense, delete_user, login_user, register_user, \
    get_flashed_message


class TestAddingExpense(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        register_user(self.browser)
        login_user(self.browser)

    def test_adding_expense(self):
        add_expense(self.browser, '7.50', 'Food (out)', 'Burrito')
        td = self.browser.find_element_by_xpath('//table//tbody//td[1]')
        self.assertTrue(float(td.text), '7.50')

    def test_cost_validation(self):
        add_expense(self.browser, 'Seven fifty', 'Food (out)', 'Burrito')
        message = get_flashed_message(self.browser)
        self.assertTrue(message, 'Cost must be a number.')

    def test_category_validation(self):
        add_expense(self.browser, '7.50', '(category)', 'Burrito')
        message = get_flashed_message(self.browser)
        self.assertTrue(message, 'Category is required.')

    def test_comment_validation(self):
        add_expense(self.browser, '7.50', 'Food (out)', '')
        message = get_flashed_message(self.browser)
        self.assertTrue(message, 'Comment is required.')

    def tearDown(self):
        delete_user(self.browser)
        self.browser.quit()
