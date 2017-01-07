"""Views reports on expenses.
"""

import datetime
import json
import collections
from calendar import monthrange

from flask import Blueprint, render_template, request
from flask.ext.login import current_user, login_required

from slate.endpoints import viewutils
from slate import dbutils, models
from slate.config import config


reports = Blueprint('reports',
                    __name__,
                    url_prefix='%s/report' % config.get('url', 'base'))


@reports.route('', methods=['GET'])
@login_required
def report_pages():
    """Delegates to functions that build appropriate reports.
    """
    year = request.args.get('year')
    month = request.args.get('month')
    if year:
        year = int(year)
        if month:
            month = int(month)
            return monthly_report(year, month)
        return yearly_report(year)
    else:
        # Default is monthly report for current month/year.
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        return monthly_report(year, month)



"""
What should a report have?
- food
  - in
  - out, discretionary
  - meals out
  - per meal
- discretionary transactions
  - sum
  - this should just be a function on the report class
"""

def monthly_report(year, month):
    """Build report for month and year.
    """
    report = models.Report(year=year, month=month)

    _, query_string = viewutils.get_date_time_strings(year, month)

    # Food
    # ------------------------------------------------------------------------
    food_in = viewutils.get_category_sum(report.expenses, 'food (in)')
    food_out = viewutils.get_category_sum(report.expenses, 'food (out)')
    food_total = food_in + food_out
    now = datetime.datetime.now()
    if now.year == year and now.month == month:
        num_days = now.day
    else:
        num_days = monthrange(year, month)[1]
    cost_per_meal = round(food_total / (num_days * 3), 2)

    # Discretionary
    # ------------------------------------------------------------------------
    discretionary = {}
    discretionary_sum = 0
    for e in report.expenses:
        if e.discretionary:
            c = e.category.name
            if c in discretionary:
                discretionary[c] += e.cost
            else:
                discretionary[c] = e.cost
            discretionary_sum += e.cost

    return render_template('report_monthly.html',
                           report=report,
                           food_in=food_in,
                           food_out=food_out,
                           cost_per_meal=cost_per_meal,
                           discretionary=discretionary,
                           discretionary_sum=discretionary_sum)


def yearly_report(year):
    """Build report for entire year.
    """
    report = models.Report(year=year)
    return render_template('report_yearly.html', report=report)


def _date_handler(date):
    """Formats date for JSON.
    """
    return [date.year, date.month, date.day]
