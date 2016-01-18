"""Manages expense endpoints.
"""

import calendar
import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required

from slate import db
from slate import models
from slate import dbutils
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
    cost, category_name, comment, errors = _validate_expense(request)
    if len(errors) > 0:
        auth_message = authutils.auth_message()
        return redirect(url_for('index.index_page',
                                auth_message=auth_message,
                                error=errors[0]))

    category = db.session\
        .query(models.Category)\
        .filter(models.Category.name == category_name)\
        .one()
    expense = models.Expense(cost, category, comment, current_user)
    db.session.add(expense)
    db.session.commit()
    return redirect(url_for('expenses.expenses_default'))


@expenses.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_expense():
    auth_message = authutils.auth_message()
    id_ = request.args.get('id')
    if request.method == 'GET':
        expense = db.session.query(models.Expense).get(id_)
        error = request.args.get('error')
        return render_template('edit.html',
                               auth_message=auth_message,
                               categories=_categories(),
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

        expense = db.session.query(models.Expense).get(id_)
        expense.cost = cost
        expense.category = db.session\
            .query(models.Category)\
            .filter_by(name=category)\
            .one()
        expense.comment = comment
        db.session.merge(expense)
        db.session.commit()
        return redirect(url_for('expenses.expenses_default'))


@expenses.route('/delete', methods=['POST'])
@login_required
def delete_expense():
    id_ = request.form.to_dict()['id']
    expense = db.session.query(models.Expense).get(id_)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('expenses.expenses_default'))


# View and plot expenses
# ----------------------------------------------------------------------------

@expenses.route('', methods=['GET'])
@login_required
def expenses_default():
    """Renders expenses for current month.
    """
    category = request.args.get('category')
    if category == 'all':
        category = None

    year = request.args.get('year')
    month = request.args.get('month')

    if year and month:
        month_str = '%s %s' % (calendar.month_name[int(month)], year)
        query_string = '?year=%s&month=%s&' % (year, month)
    else:
        now = datetime.datetime.now()
        month_str = '%s %s' % (calendar.month_name[now.month], now.year)
        query_string = '?'

    auth_message = authutils.auth_message()
    expenses = current_user.expenses(category, year, month)

    sum_ = sum([e.cost for e in expenses if e.category.name != 'rent'])
    return render_template('expenses.html',
                           auth_message=auth_message,
                           categories=_categories(),
                           category=category,
                           category_sum=sum_,
                           expenses=expenses,
                           year=year,
                           month=month,
                           month_str=month_str,
                           query_string=query_string)


@expenses.route('/all', methods=['GET'])
@login_required
def all_months():
    """Renders a list of all expenses by month.
    """
    months_all = dbutils.get_all_months()
    auth_message = authutils.auth_message()
    return render_template('expenses-all.html',
                           auth_message=auth_message,
                           months_all=months_all)


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


def _categories():
    """Returns all categories in descending order.
    """
    return db.session\
        .query(models.Category)\
        .order_by(models.Category.name)\
        .all()
