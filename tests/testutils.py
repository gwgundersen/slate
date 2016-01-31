"""Utility methods for unit testing.
"""

from selenium.common.exceptions import NoSuchElementException

from config import SLATE_URL


def exists_by_xpath(browser, xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def link_href_is_correct(browser, xpath, href):
    try:
        link = browser.find_element_by_xpath(xpath)
        actual_href = link.get_attribute('href')

        # The browser generates a complete URL from a relative path. Remove it
        # so we can just check relative paths.
        actual_href = actual_href.replace(SLATE_URL, '')

        return actual_href == '/%s' % href
    except NoSuchElementException:
        return False
