"""Utility functions for data that does not need a model.
"""

import calendar
import datetime

from flask.ext.login import current_user

from slate import db
from slate import models


def get_all_months():
    """Gets all previous months with recorded transactions.
    """
    conn = db.engine.connect()
    tuples = conn.execute(
        'SELECT '\
        '  MONTH(date_time), '\
        '  YEAR(date_time), '\
        '  SUM(cost) '\
        'FROM expense '\
        'JOIN `user` '\
        '  ON `user`.id = expense.user_fk '\
        'WHERE `user`.name = "%s" '\
        'GROUP BY MONTH(date_time), YEAR(date_time) '\
        'ORDER BY MONTH(date_time), YEAR(date_time) ASC' % current_user.name
    )

    results = []
    results = [{
        'view': '%s %s' % (calendar.month_name[c[0]], c[1]),
        'month_num': c[0],
        'year_num': c[1],
        'total': c[2]} for c in tuples.fetchall()]
    conn.close()
    return results


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
    categories = [c for c in current_user.categories if not c.hide_in_report]
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
    sql = 'SELECT DATE(date_time) as DATE, ROUND(SUM(cost), 2) '\
          '  FROM expense '\
          'JOIN `user` ' \
          '  ON `user`.id = expense.user_fk '\
          'JOIN category '\
          '  ON category.id = expense.category_fk '\
          'WHERE `user`.name = "%s" ' \
          '  AND category.name != "rent/mortgage" '\
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
