"""Utility functions for formatting view data.
"""

import calendar
import datetime


def get_expense_sum(expenses):
    """Returns sum of all expenses except rent.
    """
    return sum([e.cost for e in expenses if not e.category.hide_in_report])


def get_category_sum(expenses, category):
    """Returns sum of all expenses in category.
    """
    return sum([e.cost for e in expenses if e.category.name == category])


def get_date_time_strings(year, month):
    """Returns human-readable string for year and month, plus query string
    to load page.
    """
    if year and month:
        month_string = '%s %s' % (calendar.month_name[int(month)], year)
        query_string = '?year=%s&month=%s' % (year, month)
    else:
        now = datetime.datetime.now()
        month_string = '%s %s' % (calendar.month_name[now.month], now.year)
        query_string = ''
    return month_string, query_string


def get_num_days_in_month(year, month):
    """Returns number of days in the month provided.
    """
    now = datetime.datetime.now()
    return now.day


def get_all_days_in_month(year, month):
    """Returns a set of datetime objects, one for every day in the month.
    """
    days_in_month = get_num_days_in_month(year, month)
    dates = set()
    for day in range(1, days_in_month+1):
        d = datetime.date(year, month, day)
        dates.add(d)
    return dates


def get_all_days_in_year(year):
    dates = set()
    for day in range(1, 365+1):
        d = datetime.date(year, month, day)
        dates.add(d)
    return dates
