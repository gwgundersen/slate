"""Adds an expense.
"""


from flask import Blueprint, request
import datetime

from slate import db


add_api = Blueprint('add_api',
                    __name__,
                    url_prefix='/add')


@add_api.route('', methods=['POST'])
def add():
    """Adds expense.
    """
    cost = request.form.get('cost')
    category = request.form.get('category')
    comment = request.form.get('comment')
    datetime_ = datetime.datetime.now()
    db.save_expense(cost, category, datetime_, comment)
    return 'success'

