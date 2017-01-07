"""Utility functions for generating ordered lists of datetime objects for
reports.
"""

import calendar
import datetime


def get_num_days_in_time_period(year, month=None):
    """Returns the number of days in the time period provided.
    """
    if month:
        return get_num_days_in_month(year, month)
    else:
        days = 0
        for month in range(1, 13):
            days += len(get_ordered_dates_in_month(year, month))
        return days


def get_ordered_dates_in_year(year):
    """Returns an ordered list of datetime objects, one for every day in the
    year.
    """
    dates = []
    for month in range(1, 13):
        days_in_month = get_ordered_dates_in_month(year, month)
        dates += days_in_month
    return dates


def get_ordered_dates_in_month(year, month):
    """Returns an ordered list of datetime objects, one for every day in the
    month.
    """
    days_in_month = get_num_days_in_month(year, month)
    dates = []
    for day in range(1, days_in_month+1):
        d = datetime.date(year, month, day)
        dates.append(d)
    return dates


def get_num_days_in_month(year, month):
    """Returns number of days in the month provided.
    """
    range = calendar.monthrange(year, month)
    return range[1]
