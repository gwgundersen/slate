"""Represents a dynamically generated report.
"""

import collections
import datetime
import json

from flask_login import current_user

from slate import dates


class Report(object):

    def __init__(self, year=None, month=None):
        """Construct a report based on a specific or current month and year or
        just year.
        """
        self.expenses = current_user.expenses(year=year, month=month)
        if not (year and month):
            now = datetime.datetime.now()
            self.year = now.year
            self.month = now.month
        else:
            self.year = int(year)
            if month:
                self.month = int(month)

    @property
    def category_subtotals_json(self):
        """Returns total expenses per category, excluding rent.
        """
        subtotals = []
        for category in current_user.categories:
            expenses = [e.cost for e in self.expenses
                        if e.category.name == category.name]
            subtotals.append({
                'category': category.name.capitalize(),
                'subtotal': round(sum(expenses), 2)
            })
        return json.dumps(subtotals)

    @property
    def expenses_json(self):
        """
        """
        if self.month:
            all_days = dates.get_ordered_dates_in_month(self.year, self.month)
        else:
            all_days = dates.get_ordered_dates_in_year(self.year)

        expenses = collections.OrderedDict()
        for day in all_days:
            for e in self.expenses:
                key = str(day)
                if key not in expenses:
                    expenses[key] = []
                if e.date_time.date() != day:
                    continue
                expenses[key].append({
                    'cost': e.cost,
                    'comment': e.comment
                })
        return json.dumps(expenses)

    @property
    def total(self):
        """Returns sum of all expenses except rent.
        """
        total = sum([e.cost for e in self.expenses])
        return _format_monetary_value(total)


def _format_monetary_value(total):
    """Returns a properly formatted monetary value from a number.

    Example
    -------
    >>> _format_monetary_value(3500)
    >>> '$3,500'
    """
    return '$%s' % '{:,.2f}'.format(total)
