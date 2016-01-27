"""Views monthly reports.
"""

import datetime
import json
import collections

from flask import Blueprint, render_template, request
from flask.ext.login import current_user, login_required

from slate.endpoints import viewutils
from slate import dbutils
from slate.config import config
from slate.endpoints import authutils


reports = Blueprint('reports',
                    __name__,
                    url_prefix='%s/report' % config.get('url', 'base'))


@reports.route('', methods=['GET'])
@login_required
def report_default():
    year = request.args.get('year')
    month = request.args.get('month')
    if year and month:
        year = int(year)
        month = int(month)
    else:
        now = datetime.datetime.now()
        year = now.year
        month = now.month

    # Basic stats
    # ------------------------------------------------------------------------
    expenses_json = json.dumps(dbutils.get_category_subtotals(year, month))
    month_string, query_string = viewutils.get_date_time_strings(year, month)
    auth_message = authutils.auth_message()
    expenses = current_user.expenses(year=year, month=month)
    category_sum = viewutils.get_expense_sum(expenses)

    # Total expenses per day for the month
    # ------------------------------------------------------------------------

    # TODO: This section feels messy, but I'm rushing to finish for
    # Hack && Tell.

    all_expenses = current_user.expenses(year=year, month=month)
    grouped_expenses = collections.OrderedDict()
    for e in all_expenses:
        if e.category.name == 'rent':
            continue
        key = e.date_time.strftime('%Y-%m-%d')
        if key not in grouped_expenses:
            grouped_expenses[key] = []
        grouped_expenses[key].append({
            'cost': e.cost,
            'comment': e.comment
        })

    all_days = viewutils.get_all_days_in_month(year, month)
    for d in all_days:
        d = str(d)
        if d not in grouped_expenses:
            grouped_expenses[d] = []

    ordered_expenses = []
    for i,date in enumerate(sorted(grouped_expenses)):
        ordered_expenses.append({
            'date_time': date,
            'expenses': grouped_expenses[date]
        })

    ordered_expenses_json = json.dumps(ordered_expenses)

    # Food
    # ------------------------------------------------------------------------
    food_in = viewutils.get_category_sum(expenses, 'food (in)')
    food_out = viewutils.get_category_sum(expenses, 'food (out)')
    food_total = food_in + food_out
    num_days_so_far = datetime.datetime.now().day
    cost_per_meal = round(food_total / (num_days_so_far * 3), 2)

    # Discretionary
    # ------------------------------------------------------------------------
    alcohol = viewutils.get_category_sum(expenses, 'alcohol')
    entertainment = viewutils.get_category_sum(expenses, 'entertainment')
    discretionary = {}
    discretionary_sum = 0
    for e in expenses:
        if e.discretionary:
            c = e.category.name
            if c in discretionary:
                discretionary[c] += e.cost
            else:
                discretionary[c] = e.cost
            discretionary_sum += e.cost

    return render_template('report.html',
                           auth_message=auth_message,
                           month_string=month_string,
                           category_sum=category_sum,
                           food_in=food_in,
                           food_out=food_out,
                           cost_per_meal=cost_per_meal,
                           alcohol=alcohol,
                           entertainment=entertainment,
                           discretionary=discretionary,
                           discretionary_sum=discretionary_sum,
                           query_string=query_string,
                           expenses_json=expenses_json,
                           ordered_expenses_json=ordered_expenses_json)

def _date_handler(date):
    """Formats date for JSON.
    """
    return [date.year, date.month, date.day]
