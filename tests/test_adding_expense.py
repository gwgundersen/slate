"""Unit tests for verifying that an expense can be added correctly. This is
the one pipeline we never want to break.
"""

import unittest

from selenium import webdriver

from testutils import login_user, add_expense
from config import SLATE_URL


class TestAddingExpense(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_adding_expense(self):
        login_user(self.browser)
        add_expense(self.browser, 7.50, 'Food (out)', 'Burrito')
        td = self.browser.find_element_by_xpath('//table//tbody//td[1]')
        self.assertTrue(float(td.text), 7.50)

    def test_cost_validation(self):
        login_user(self.browser)
        add_expense(self.browser, 'Seven fifty', 'Food (out)', 'Burrito')
        message = self\
            .browser.find_element_by_xpath('//p[@class="highlight"]')
        self.assertTrue(message.text, 'Cost must be a number.')

    def test_category_validation(self):
        login_user(self.browser)
        add_expense(self.browser, 7.50, '(category)', 'Burrito')
        message = self\
            .browser.find_element_by_xpath('//p[@class="highlight"]')
        self.assertTrue(message.text, 'Category is required.')

    def test_comment_validation(self):
        login_user(self.browser)
        add_expense(self.browser, 7.50, 'Food (out)', '')
        message = self\
            .browser.find_element_by_xpath('//p[@class="highlight"]')
        self.assertTrue(message.text, 'Comment is required.')

    def tearDown(self):
        self.browser.quit()
