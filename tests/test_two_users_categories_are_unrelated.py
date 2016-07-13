"""Unit tests for verifying that the category sets for different users are in
fact different, i.e. if user A deletes or updates his/her category, it does
not effect the categories of user B.
"""

import unittest

from selenium import webdriver
from selenium.webdriver.support.select import Select

from utils import delete_user, register_user, SLATE_URL, \
    get_flashed_message, add_expense, logout_user, exists_by_xpath, login_user


class TestTwoUsersCategoriesAreUnrelated(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_two_users_categories_are_unrelated(self):
        # Create user A, add an expense with "Food (out)" category. We'll
        # delete this category for user B.
        # --------------------------------------------------------------------
        register_user(self.browser, username='userA', password1='pw',
                      password2='pw')
        add_expense(self.browser, '7.50', 'Food (out)', 'Burrito')
        logout_user(self.browser)

        # Create user B, delete "Food (out)" category.
        # --------------------------------------------------------------------
        register_user(self.browser, username='userB', password1='pw',
                      password2='pw')

        self.browser.get('%s/account/settings' % SLATE_URL)
        self.browser.find_element_by_xpath('//tr//td[text()="Food (out)"]/..//a[text()="Edit"]').click()
        self.browser.find_element_by_xpath('//input[@value="Delete"]').click()
        self.browser.switch_to.alert.accept()
        logout_user(self.browser)

        # Verify that user A still has "Food (out)" category.
        # --------------------------------------------------------------------
        login_user(self.browser, 'userA', 'pw')
        self.browser.get('%s/expenses' % SLATE_URL)
        self.assertTrue(exists_by_xpath(self.browser, '//td[text()="7.50"]'))
        self.assertTrue(exists_by_xpath(self.browser, '//td[text()="Burrito"]'))
        self.assertTrue(exists_by_xpath(self.browser, '//td[text()="Food (out)"]'))

        # Cleanup.
        # --------------------------------------------------------------------
        # Delete user A.
        delete_user(self.browser)
        # Delete user B.
        login_user(self.browser, 'userB', 'pw')
        delete_user(self.browser)

    def tearDown(self):
        self.browser.quit()
