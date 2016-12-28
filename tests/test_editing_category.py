"""Unit tests for verifying a new category can be created.
"""

import time
import unittest

from selenium import webdriver
from selenium.webdriver.support.select import Select

from utils import delete_user, register_user, click, SLATE_URL, \
    exists_by_xpath, add_expense, wait_until


class TestEditingCategory(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        register_user(self.browser)
        self.browser.get('%s/account/settings' % SLATE_URL)

    def test_edit_category(self):
        click(self.browser, '//a[text()="Edit"][1]', '//h3[text()="Edit category"]')
        cost_input = self.browser.find_element_by_xpath('//input[@name="category_name"]')
        cost_input.clear()
        cost_input.send_keys('edited test category')
        click(self.browser, '//button[text()="Edit"]', '//h3[text()="Edit category"]')
        time.sleep(2)  # No idea why this is necessary.
        self.assertTrue(exists_by_xpath(self.browser, '//tr[1]//td[text()="Edited test category"]'))

    def test_cancelling_edit(self):
        click(self.browser, '//a[text()="Edit"][1]', '//h3[text()="Edit category"]')
        click(self.browser, '//a[text()="Cancel"]', '//h2[text()="Settings"]')
        self.assertTrue(exists_by_xpath(self.browser, '//tr[1]//td[text()="Alcohol"]'))

    def test_deleting_expense(self):
        self.browser.get(SLATE_URL)
        # We want to verify that this expense is deleted.
        add_expense(self.browser, '7.50', 'Food (out)', 'Burrito')
        self.browser.get('%s/account/settings' % SLATE_URL)
        click(self.browser, '//tr//td[text()="Food (out)"]/..//a[text()="Edit"]')
        click(self.browser, '//input[@value="Delete"]', '//h3[text()="Edit category"]')
        self.browser.switch_to.alert.accept()
        self.browser.get(SLATE_URL)
        select = Select(
            wait_until(self.browser, '//select[@name="category_id"]')
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
