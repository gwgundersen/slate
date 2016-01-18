"""Utility functions for data that does not need a model.
"""

import datetime

from flask.ext.login import current_user

from slate import db
from slate import models


def get_all_months():
    """Gets all previous months with recorded transactions.
    """
    conn = db.engine.connect()
    results = conn.execute(
        'SELECT DISTINCT '\
        '  CONCAT(MONTHNAME(date_time), " ", YEAR(date_time)), '\
        '  MONTH(date_time), '\
        '  YEAR(date_time) FROM expense '\
        'ORDER BY date_time DESC'
    )
    return [{
        'view': c[0],
        'month_num': c[1],
        'year_num': c[2]} for c in results.fetchall()]


def get_category_subtotals(year=None, month=None):
    """Returns total expenses per category, excluding rent.
    """
    result = {}
    if not year or not month:
        now = datetime.datetime.now()
        year = now.year
        month = now.month
    categories = db.session.query(models.Category).all()
    categories = [c for c in categories if c.name != 'rent']
    for category in categories:
        expenses = [e.cost for e in category.expenses if
                    e.user.name == current_user.name and
                    e.date_time.year == year and
                    e.date_time.month == month]
        result[category.name.capitalize()] = round(sum(expenses), 2)
    return result
