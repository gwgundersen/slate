"""Adds an expense.
"""


from flask import Blueprint, request, redirect, url_for
from flask.ext.login import current_user, login_required
import datetime

from slate import db
from slate.config import config


add = Blueprint('add',
                __name__,
                url_prefix=config.get('url', 'base'))


@add.route('/add', methods=['POST'])
@login_required
def add_api():
    """Adds expense.
    """
    error_messages = []
    try:
        cost = request.form['cost']
        cost = float(cost)
    except ValueError:
        error_messages.append('Cost must be a float.')

    category = request.form['category']
    if category == 'select':
        error_messages.append('Category is required.')

    comment = request.form.get('comment')
    if not comment:
        error_messages.append('Comment is required')

    if len(error_messages) > 0:
        auth_message = '%s is logged in.' % current_user.name
        return redirect(url_for('index.index_page'))

    datetime_ = datetime.datetime.now()
    db.save_expense(cost, category, datetime_, comment)
    return redirect(url_for('expenses.expenses_default'))

