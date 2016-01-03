"""Views expenses.
"""


from flask import Blueprint, render_template
from flask.ext.login import login_required

from slate import db
from slate.config import config


expenses = Blueprint('expenses',
                     __name__,
                     url_prefix='%s/expenses' % config.get('url', 'base'))


@expenses.route('/', methods=['GET'])
@login_required
def expenses_default():
    """Views expenses by current month.
    """
    categories = db.get_categories()
    expenses = db.get_expenses()
    return render_template('expenses.html',
                           categories=categories,
                           expenses=expenses)

@expenses.route('/<category>', methods=['GET'])
@login_required
def expenses_by_category(category):
    """Views expenses by current month and category.
    """
    expenses = db.get_expenses_by_category(category)
    categories = db.get_categories()
    return render_template('expenses.html',
                           categories=categories,
                           expenses=expenses)

