"""Manages expense endpoints.
"""

from flask import Blueprint, flash, redirect, render_template, request, \
    url_for
from flask.ext.login import current_user, login_required

from slate import db
from slate import models
from slate import dbutils
from slate.config import config


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
        flash(errors[0], 'error')
        return redirect(url_for('index.index_page'))

    expense = models.Expense(cost, category, comment, current_user)
    db.session.add(expense)
    db.session.commit()
    return redirect(url_for('expenses.expenses_default'))


@expenses.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_expense():
    id_ = request.args.get('id')
    if request.method == 'GET':
        expense = db.session.query(models.Expense).get(id_)
        return render_template('expense-edit.html',
                               categories=current_user.categories,
                               expense=expense)
    if request.method == 'POST':
        id_ = request.form.get('id')
        cost, category, comment, errors = _validate_expense(request)
        if len(errors) > 0:
            flash(errors[0], 'error')
            return redirect(url_for('expenses.edit_expense', id=id_))

        expense = db.session.query(models.Expense).get(id_)
        expense.cost = cost
        expense.category = (category or expense.category)
        expense.comment = comment
        db.session.merge(expense)
        db.session.commit()
        return redirect(url_for('expenses.expenses_default'))


@expenses.route('/delete', methods=['POST'])
@login_required
def delete_expense():
    """Deletes expense.
    """
    id_ = request.form.to_dict()['id']
    expense = db.session.query(models.Expense).get(id_)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense successfully deleted.', 'success')
    return redirect(url_for('expenses.expenses_default'))


# View and plot expenses
# ----------------------------------------------------------------------------

@expenses.route('', methods=['GET'])
@login_required
def expenses_default():
    """Renders expenses for current month.
    """
    category_id = request.args.get('category_id')
    if not category_id or category_id == 'all':
        category = None
    else:
        category = db.session.query(models.Category).get(category_id)
    year = request.args.get('year')
    month = request.args.get('month')
    report = models.Report(year=year, month=month, category=category)
    return render_template('expenses.html',
                           report=report,
                           categories=current_user.categories)


@expenses.route('/previous', methods=['GET'])
@login_required
def all_months():
    """Renders a list of all expenses by month.
    """
    months_all = dbutils.get_all_months()
    years = set()
    for obj in months_all:
        years.add(obj['year_num'])
    return render_template('months-all.html',
                           months_all=months_all,
                           years_all=sorted(years))


@expenses.route('/all', methods=['GET'])
@login_required
def all_expenses():
    """Renders a list of all expenses by month.
    """
    expenses = current_user.all_expenses()
    return render_template('expenses-all.html', expenses=expenses)


# Utility methods
# ----------------------------------------------------------------------------

def _validate_expense(request):
    """Validates the arguments in a request to add or edit an expense.
    """
    errors = []
    try:
        cost = request.form['cost']
        cost = float(cost)
        cost = round(cost, 2)
    except ValueError:
        errors.append('Cost must be a number.')

    category_id = request.form['category_id']
    if category_id == 'select':
        errors.append('Category is required.')
        category = None
    else:
        category = db.session.query(models.Category).get(category_id)

    comment = request.form.get('comment')
    if not comment:
        errors.append('Comment is required.')

    return cost, category, comment, errors
