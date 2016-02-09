"""Unit tests for verifying user interface has the correct buttons, links, etc.
"""

import unittest

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

from testutils import exists_by_xpath, link_href_is_correct, login_user, \
    logout_user
from config import SLATE_URL


class TestBasicUserInterface(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(SLATE_URL)

    def test_title(self):
        self.assertEqual(self.browser.title, 'Slate')

    def test_header(self):
        self.assertTrue(
            exists_by_xpath(self.browser, '//h1//a[contains(text(), "Slate")]')
        )
        try:
            logout_user(self.browser)
        except NoSuchElementException:
            pass
        self.assertTrue(
            exists_by_xpath(self.browser, '//span[text()="No user logged in."]')
        )

    def test_form_fields(self):
        login_user(self.browser)
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

    # def test_add_and_view_buttons(self):
    #     login_user(self.browser)
    #     self.assertTrue(
    #         exists_by_xpath(self.browser, '//button[text()="Add"]')
    #     )
    #     self.assertTrue(
    #         exists_by_xpath(self.browser, '//a[text()="View expenses"]')
    #     )
    #
    # def test_footer_links_logged_in(self):
    #     login_user(self.browser)
    #     self.assertTrue(
    #         link_href_is_correct(self.browser, '//a[text()="Logout"]', 'logout')
    #     )
    #
    # def test_footer_links_logged_out(self):
    #     self.assertTrue(
    #         link_href_is_correct(self.browser, '//a[text()="Login"]', 'login')
    #     )
    #     self.assertTrue(
    #         link_href_is_correct(self.browser, '//a[text()="Register"]', 'register')
    #     )

    def tearDown(self):
        self.browser.quit()
