"""Represents a dynamically generated report.
"""

import calendar
import collections
import datetime
import json

from flask_login import current_user

from slate import dates, dbutils
from slate.endpoints import viewutils


MIN_NUM_REPEATED = 5


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
        self._BUDGET = 2632

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
        """Returns the sum of all expenses, formatted as a monetary value.
        """
        return _format_monetary_value(self._total)

    @property
    def remaining(self):
        """Returns the remaining budget, formatted as a monetary value.
        """
        return _format_monetary_value(self._BUDGET - self._total)

    @property
    def count(self):
        """Returns the number of expenses.
        """
        return len(self.expenses)

    @property
    def num_expenses_per_day(self):
        """Returns the number of expenses per day.
        """
        value = self.count / float(self.days)
        return round(value, 3)

    @property
    def average(self):
        """Returns the average cost of an expense.
        """
        value = self._total / float(self.days)
        return round(value, 2)

    @property
    def median(self):
        """Returns the median cost of an expense.
        """
        numbers = [e.cost for e in self.expenses]
        numbers = sorted(numbers)
        center = len(numbers) / 2
        if len(numbers) % 2 == 0:
            # Return the average of the middle two numbers.
            value = sum(numbers[center - 1:center + 1]) / 2.0
            return round(value, 2)
        else:
            return numbers[center]

    @property
    def max_(self):
        """Returns the max expense in the reporting time period.
        """
        if not self.expenses:
            return 0.0
        return max([e.cost for e in self.expenses])

    @property
    def days(self):
        """Returns the number of days in the reporting time period.
        """
        return dates.get_num_days_in_time_period(self.year, self.month)

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
                'subtotal': round(sum(expenses), 2),
                'budget': category.budget
            })
        return subtotals

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

    def get_repeated_expenses(self, min_num_repeated=MIN_NUM_REPEATED):
        """Returns comments and subtotals for expenses that are repeated at
        least `min_num_repeated` times.
        """
        expenses = dbutils.get_repeated_expenses(self.year, min_num_repeated)
        expenses = {comment: _format_monetary_value(cost)
                    for comment, cost in expenses.items()}
        return expenses

    @property
    def food(self):
        """Returns analysis of food expenditures.
        """
        food_categories = {}
        total = 0
        for category in current_user.categories:
            if 'food' not in category.name:
                continue
            subtotal = viewutils.get_category_sum(self.expenses, category.name)
            food_categories[category.name] = _format_monetary_value(subtotal)
            total += subtotal
        per_meal = _format_monetary_value(total / (self.days * 3))
        return _format_monetary_value(total), food_categories, per_meal

    @property
    def supports_food_analysis(self):
        """Returns True if any user category includes the word food.
        """
        for category in current_user.categories:
            if 'food' in category.name:
                return True
        return False

    @property
    def _total(self):
        """Returns sum of all expenses.
        """
        if self.category:
            costs = [e.cost for e in self.expenses
                     if e.category.name == self.category.name]
        else:
            costs = [e.cost for e in self.expenses]
        return sum(costs)


def _format_monetary_value(total):
    """Returns a properly formatted monetary value from a number.

    Example
    -------
    >>> _format_monetary_value(3500)
    >>> '$3,500'
    """
    return '$%s' % '{:,.2f}'.format(total)
