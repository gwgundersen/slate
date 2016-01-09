"""Manages expense endpoints.
"""

import calendar
import datetime
import json

from flask import Blueprint, redirect, render_template, request, url_for
from flask.ext.login import login_required

from slate import db
from slate.config import config


expenses = Blueprint('expenses',
                     __name__,
                     url_prefix='%s/expenses' % config.get('url', 'base'))


@expenses.route('', methods=['GET'])
@login_required
def expenses_default():
    """Renders expenses for current month.
    """
    category = request.args.get('category')
    year = request.args.get('year')
    month = request.args.get('month')
    if year and month:
        month_str = '%s %s' % (calendar.month_name[int(month)], year)
        query_string = '?year=%s&month=%s&' % (year, month)
    else:
        now = datetime.datetime.now()
        month_str = '%s %s' % (calendar.month_name[now.month], now.year)
        query_string = '?'
    categories = db.get_categories()
    sum_, expenses = db.get_expenses(category, year, month)
    return render_template('expenses.html',
                           categories=categories,
                           category_sum=sum_,
                           expenses=expenses,
                           year=year,
                           month=month,
                           month_str=month_str,
                           query_string=query_string)


@expenses.route('/all', methods=['GET'])
@login_required
def previous_expenses_list():
    """Renders a list of all expenses by month.
    """
    months_all = db.get_previous_months()
    return render_template('expenses-all.html',
                           months_all=months_all)


@expenses.route('/plot', methods=['GET'])
@login_required
def plot_previous_expenses():
    """Plots a time series of all previous expenses.
    """
    expenses_all = db.get_all_expenses_by_category()
    expenses_all = json.dumps(expenses_all, default=_date_handler)
    return render_template('expenses-plot.html',
                           data=expenses_all)


@expenses.route('/delete', methods=['POST'])
@login_required
def delete_expense():
    id_ = request.form.to_dict()['id']
    db.delete_expense(id_)
    return redirect(url_for('expenses.expenses_default'))


@expenses.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_expense():
    id_ = request.args.get('id')
    if request.method == 'GET':
        expense = db.get_expense(id_)
        print(expense)
        return str(expense)


def _date_handler(date):
    """Formats date for JSON.
    """
    return [date.year, date.month, date.day]

