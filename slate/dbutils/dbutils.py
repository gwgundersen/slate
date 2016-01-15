"""Utility functions for data that does not need a model.
"""

from slate import db
from slate import models


def get_previous_months():
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


def get_expenses_by_category():
    """Returns all expenses in the database.
    """
    result = {}
    categories = db.session.query(models.Category).all()
    for category in categories:
        result[category.name] = category.current_expenses
    return result
