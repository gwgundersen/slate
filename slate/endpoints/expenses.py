"""Views expenses.
"""


from flask import Blueprint, render_template, request
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
    #cat = request.args['category']
    distinct_months = db.get_month_years()
    categories = db.get_categories()
    sum_, expenses = db.get_expenses()
    return render_template('expenses.html',
                           categories=categories,
                           category_sum=sum_,
                           distinct_months=distinct_months,
                           expenses=expenses)


@expenses.route('/<category>', methods=['GET'])
@login_required
def expenses_by_category(category):
    """Views expenses by current month and category.
    """
    categories = db.get_categories()
    sum_, expenses = db.get_expenses_by_category(category)
    return render_template('expenses.html',
                           categories=categories,
                           category_sum=sum_,
                           expenses=expenses)

