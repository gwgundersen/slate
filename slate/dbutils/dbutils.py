"""Utility functions for data that does not need a model.
"""

from slate import db


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


# def get_all_expenses_by_category():
#     """Returns all expenses in the database.
#     """
#     categories = {}
#     for category in get_categories():
#         if category not in categories:
#             categories[category] = []
#         data = _get_all_expenses_for_category(category)
#         categories[category].append(data)
#     return categories
