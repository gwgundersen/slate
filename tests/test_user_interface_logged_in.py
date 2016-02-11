"""Unit tests for verifying user interface is correct when user is logged in.
"""

import unittest

from selenium import webdriver
from selenium.webdriver.support.select import Select

from utils import exists_by_xpath, register_user, delete_user, \
    MOCK_USER, SLATE_URL


class TestBasicUserInterface(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        register_user(self.browser)
        self.browser.get(SLATE_URL)

    def test_title(self):
        self.assertEqual(self.browser.title, 'Slate')

    def test_header(self):
        self.assertTrue(
            exists_by_xpath(self.browser, '//h1//a[contains(text(), "Slate")]')
        )
        span = self.browser.find_element_by_xpath('//div[@id="header"]//span')
        self.assertEqual(span.text, MOCK_USER)
        self.assertTrue(
            exists_by_xpath(self.browser, '//a[text()="Account"]')
        )
        self.assertTrue(
            exists_by_xpath(self.browser, '//a[text()="Settings"]')
        )
        self.assertTrue(
            not exists_by_xpath(self.browser, '//a[text()="Login"]')
        )
        self.assertTrue(
            not exists_by_xpath(self.browser, '//a[text()="Register"]')
        )

    def test_form_fields(self):
        input_ = self.browser.find_element_by_xpath('//input[@name="cost"]')
        self.assertEqual(input_.get_attribute('placeholder'), 'Cost ($)')

        select = Select(
            self.browser.find_element_by_xpath('//select[@name="category_id"]')
        )
        self.assertEqual(select.first_selected_option.text, '(category)')

        input_ = self.browser.find_element_by_xpath('//input[@name="comment"]')
        self.assertEqual(input_.get_attribute('placeholder'), 'Comment')

        input_ = self.browser\
            .find_element_by_xpath('//input[@name="discretionary"]')
        self.assertEqual(input_.get_attribute('checked'), 'true')

    def test_add_and_view_buttons(self):
        self.assertTrue(
            exists_by_xpath(self.browser, '//button[text()="Add"]')
        )
        self.assertTrue(
            exists_by_xpath(self.browser, '//a[text()="View expenses"]')
        )

    def test_footer_links(self):
        self.assertTrue(
            exists_by_xpath(self.browser, '//div[@id="footer"]//button[text()="Logout"]')
        )

    def tearDown(self):
        delete_user(self.browser)
        self.browser.quit()
