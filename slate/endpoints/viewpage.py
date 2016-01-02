"""Views expenses.
"""


from flask import Blueprint, render_template

from slate import db
from slate.config import config


view_page = Blueprint('view_page',
                      __name__,
                      url_prefix='%s/view' % config.get('url', 'base'))


@view_page.route('/', methods=['GET'])
def view_default():
    """Views expenses by current month.
    """
    categories = db.get_categories()
    expenses = db.get_expenses()
    return render_template('view.html',
                           categories=categories,
                           expenses=expenses)

@view_page.route('/<category>', methods=['GET'])
def view_by_category(category):
    """Views expenses by current month and category.
    """
    expenses = db.get_expenses_by_category(category)
    categories = db.get_categories()
    return render_template('view.html',
                           categories=categories,
                           expenses=expenses)

