"""Manages expense endpoints.
"""

import calendar
import datetime
import json

from flask import Blueprint, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required

from slate import db
from slate.config import config
from slate.endpoints import authutils


expenses = Blueprint('expenses',
                     __name__,
                     url_prefix='%s/expenses' % config.get('url', 'base'))


# Add, edit, delete
# ----------------------------------------------------------------------------

@expenses.route('/add', methods=['POST'])
@login_required
def add_expense():
    """Adds expense.
    """
    cost, category, comment, errors = _validate_expense(request)
    if len(errors) > 0:
        auth_message = authutils.auth_message()
        return redirect(url_for('index.index_page',
                                auth_message=auth_message,
                                error=errors[0]))

    datetime_ = datetime.datetime.now()
    db.save_expense(cost, category, datetime_, comment)
    return redirect(url_for('expenses.expenses_default'))


@expenses.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_expense():
    auth_message = authutils.auth_message()
    id_ = request.args.get('id')
    if request.method == 'GET':
        categories = db.get_categories()
        expense = db.get_expense(id_)
        error = request.args.get('error')
        return render_template('edit.html',
                               auth_message=auth_message,
                               categories=categories,
                               error=error,
                               expense=expense)
    if request.method == 'POST':
        id_ = request.form.get('id')
        cost, category, comment, errors = _validate_expense(request)
        if len(errors) > 0:
            url = url_for('expenses.edit_expense',
                          id=id_,
                          auth_message=auth_message,
                          error=errors[0])
            return redirect(url)

        db.edit_expense(id_, cost, category, comment)
        return redirect(url_for('expenses.expenses_default'))


@expenses.route('/delete', methods=['POST'])
@login_required
def delete_expense():
    id_ = request.form.to_dict()['id']
    db.delete_expense(id_)
    return redirect(url_for('expenses.expenses_default'))


# View and plot expenses
# ----------------------------------------------------------------------------

@expenses.route('', methods=['GET'])
@login_required
def expenses_default():
    """Renders expenses for current month.
    """
    category = request.args.get('category')
    year = request.args.get('year')
    month = request.args.get('month')
    auth_message = authutils.auth_message()
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
                           auth_message=auth_message,
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
    auth_message = authutils.auth_message()
    return render_template('expenses-all.html',
                           auth_message=auth_message,
                           months_all=months_all)


@expenses.route('/plot', methods=['GET'])
@login_required
def plot_previous_expenses():
    """Plots a time series of all previous expenses.
    """
    expenses_all = db.get_all_expenses_by_category()
    expenses_all = json.dumps(expenses_all, default=_date_handler)
    auth_message = authutils.auth_message()
    return render_template('expenses-plot.html',
                           auth_message=auth_message,
                           data=expenses_all)


# Utility methods
# ----------------------------------------------------------------------------

def _validate_expense(request):
    """Validates the arguments in a request to add or edit an expense.
    """
    errors = []
    try:
        cost = request.form['cost']
        cost = float(cost)
    except ValueError:
        errors.append('Cost must be a float.')

    category = request.form['category']
    if category == 'select':
        errors.append('Category is required.')

    comment = request.form.get('comment')
    if not comment:
        errors.append('Comment is required')

    return cost, category, comment, errors


def _date_handler(date):
    """Formats date for JSON.
    """
    return [date.year, date.month, date.day]

