"""Utility methods for unit testing.
"""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

from config import SLATE_URL, MOCK_USER, MOCK_PW


def exists_by_xpath(browser, xpath):
    """Returns True if element exists, False otherwise.
    """
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def link_href_is_correct(browser, xpath, href):
    """Returns True if link href is the value passed in, False otherwise.
    """
    try:
        link = browser.find_element_by_xpath(xpath)
        actual_href = link.get_attribute('href')

        # The browser generates a complete URL from a relative path. Remove it
        # so we can just check relative paths.
        actual_href = actual_href.replace(SLATE_URL, '')

        return actual_href == '/%s' % href
    except NoSuchElementException:
        return False


def login_user(browser):
    """Logins in user.
    """
    browser.get('%s/login' % SLATE_URL)
    username_input = browser\
        .find_element_by_xpath('//input[@name="username"]')
    password_input = browser\
        .find_element_by_xpath('//input[@name="password"]')
    username_input.send_keys(MOCK_USER)
    password_input.send_keys(MOCK_PW)
    browser.find_element_by_xpath('//button[@type="submit"]').click()


def logout_user(browser):
    """Logs out user.
    """
    browser.find_element_by_xpath('//div[@id="footer"]//button[@type="submit"]').click()


def add_expense(browser, cost, category, comment):
    """Adds expense.
    """
    cost_input = browser.find_element_by_xpath('//input[@name="cost"]')
    cost_input.send_keys(cost)
    category_select = Select(
        browser.find_element_by_xpath('//select[@name="category_id"]')
    )
    category_select.select_by_visible_text(category)
    comment_input = browser\
        .find_element_by_xpath('//input[@name="comment"]')
    comment_input.send_keys(comment)
    browser.find_element_by_xpath('//button[text()="Add"]').click()
