"""Represents a dynamically generated report.
"""

import calendar
import collections
import datetime
import json

from flask_login import current_user

from slate import dates


class Report(object):

    def __init__(self, year=None, month=None, category=None):
        """Construct a report based on a specific or current month and year or
        just year.
        """
        self.expenses = current_user.expenses(year=year, month=month,
                                              category=category)
        if not year and not month:
            now = datetime.datetime.now()
            self.year = now.year
            self.month = now.month
        else:
            self.year = int(year)
            self.month = int(month) if month else None
        self.category = category

    @property
    def description(self):
        """Returns text description of report.
        """
        if self.month:
            desc = '%s %s' % (calendar.month_name[self.month], self.year)
        elif self.year:
            desc = self.year
        if self.category:
            desc = '%s (%s)' % (desc, self.category.name)
        return desc

    @property
    def total(self):
        """Returns sum of all expenses except rent.
        """
        if self.category:
            costs = [e.cost for e in self.expenses
                     if e.category.name == self.category.name]
        else:
            costs = [e.cost for e in self.expenses]
        return _format_monetary_value(sum(costs))

    @property
    def query_string(self):
        """Returns a query string that properly references report itself.
        """
        qs = '?year=%s' % self.year
        if self.month:
            qs += '&month=%s' % self.month
        return qs


    def get_category_subtotals(self, format='json'):
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
        return json.dumps(subtotals) if format == 'json' else subtotals

    def get_ordered_expenses(self, format='json'):
        """Returns expenses as JSON.
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
                if format == 'json':
                    expenses[key].append({
                        'cost': e.cost,
                        'comment': e.comment,
                        'category': e.category.name
                    })
                else:
                    expenses[key].append(e)
        return json.dumps(expenses) if format == 'json' else expenses


def _format_monetary_value(total):
    """Returns a properly formatted monetary value from a number.

    Example
    -------
    >>> _format_monetary_value(3500)
    >>> '$3,500'
    """
    return '$%s' % '{:,.2f}'.format(total)
