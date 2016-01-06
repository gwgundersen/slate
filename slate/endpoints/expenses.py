"""Views expenses.
"""


from flask import Blueprint, render_template, request
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
    categories = db.get_categories()
    sum_, expenses = db.get_expenses(category, year, month)
    return render_template('expenses.html',
                           categories=categories,
                           category_sum=sum_,
                           expenses=expenses)


@expenses.route('/all', methods=['GET'])
@login_required
def previous_expenses_list():
    """Renders a list of all expenses by month.
    """
    expenses_all = db.get_previous_months()
    return render_template('expenses-all.html',
                           expenses_all=expenses_all)

