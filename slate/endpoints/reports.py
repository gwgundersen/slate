"""Views monthly reports.
"""

import datetime
import json
import time

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
    sums_per_day = dbutils.get_sum_per_day(year, month)
    all_days = viewutils.get_all_days_in_month(year, month)
    date_set = set([x['date_time'] for x in sums_per_day])
    for day in all_days:
        if day not in date_set:
            sums_per_day.append({
                'date_time': day,
                'total': 0
            })

    sums_per_day.sort(key=lambda x: x['date_time'])
    sums_per_day_json = json.dumps(sums_per_day, default=_date_handler)

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
    discretionary = food_out + alcohol + entertainment

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
                           expenses_json=expenses_json,
                           sums_per_day_json=sums_per_day_json)

def _date_handler(date):
    """Formats date for JSON.
    """
    return [date.year, date.month, date.day]
