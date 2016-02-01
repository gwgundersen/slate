"""Utility methods for unit testing.
"""

from selenium.common.exceptions import NoSuchElementException

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
