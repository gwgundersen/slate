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
        '  CONCAT(MONTHNAME(date_time), " ", YEAR(date_time)) dt, '\
        '  MONTH(date_time), '\
        '  YEAR(date_time) '
        'FROM expense '\
        'JOIN `user` '\
        '  ON `user`.id = expense.user_fk '\
        'WHERE `user`.name = "%s" '\
        'ORDER BY dt DESC' % current_user.name
    )
    return [{
        'view': c[0],
        'month_num': c[1],
        'year_num': c[2]} for c in results.fetchall()]


def get_category_subtotals(year=None, month=None):
    """Returns total expenses per category, excluding rent.
    """
    results = []
    if not (year and month):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
    else:
        year = int(year)
        month = int(month)
    categories = get_categories()
    categories = [c for c in categories if c.name != 'rent']
    for category in categories:
        expenses = [e.cost for e in category.expenses if
                    e.user.name == current_user.name and
                    e.date_time.year == year and
                    e.date_time.month == month]
        results.append({
            'category': category.name.capitalize(),
            'subtotal': round(sum(expenses), 2)
        })
    return results


def get_sum_per_day(year, month):
    conn = db.engine.connect()
    sql = 'SELECT DATE(date_time) as DATE, SUM(cost) '\
          '  FROM expense '\
          'JOIN `user` ' \
          '  ON `user`.id = expense.user_fk '\
          'JOIN category '\
          '  ON category.id = expense.category_fk '\
          'WHERE `user`.name = "%s" ' \
          '  AND category.name != "rent" '\
          '  AND YEAR(date_time) = %s ' \
          '  AND MONTH(date_time) = %s '\
          'GROUP BY DATE(date_time)' % (
              current_user.name,
              year,
              month
          )
    results = conn.execute(sql)
    return [{
        'date_time': c[0],
        'total': c[1]} for c in results.fetchall()]


def get_categories():
    """Returns all categories in descending order.
    """
    return db.session\
        .query(models.Category)\
        .order_by(models.Category.name)\
        .all()
