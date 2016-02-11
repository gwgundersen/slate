"""Unit tests for verifying a new category can be created.
"""

import unittest

from selenium import webdriver

from utils import delete_user, register_user, get_flashed_message


class TestCreatingNewUser(unittest.TestCase):

    pass
    # def setUp(self):
    #     self.browser = webdriver.Firefox()
    #     register_user(self.browser)
    #
    # def test_create_new_category(self):
    #     input = self.browser.find_element_by_xpath(
    #         '//input[@name="category_id"]'
    #     )
    #     import pdb; pdb.set_trace()
    #
    # def tearDown(self):
    #     delete_user(self.browser)
    #     self.browser.quit()
