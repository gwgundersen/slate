"""Handles all database transactions.
"""


from contextlib import closing
import MySQLdb

from slate.config import db_connection_args


# User transactions
# -----------------

def get_user(username):
    """Gets user based on username.
    """
    with closing(connection()) as conn:
        with closing(conn.cursor()) as cur:
            sql = 'SELECT id, name, password, salt '\
                  'FROM user WHERE name = "%s"' % (username)
            cur.execute(sql)
            return cur.fetchone()


def get_user_by_id(id_):
    """Gets user based on user ID.
    """
    with closing(connection()) as conn:
        with closing(conn.cursor()) as cur:
            sql = 'SELECT id, name, password FROM user WHERE id = %s' % (id_)
            cur.execute(sql)
            return cur.fetchone()


# Saving expenses
# ---------------

def save_expense(cost, category, datetime, comment):
    """Saves an expense.
    """
    with closing(connection()) as conn:
        with closing(conn.cursor()) as cur:
            sql = 'INSERT INTO expense (cost, category_fk, datetime, comment) '\
                  '  VALUES (%s, (%s), "%s", "%s")' % (
                      cost,
                      'SELECT id FROM category WHERE name = "%s"' % category,
                      datetime,
                      comment
                  )
            cur.execute(sql)
            conn.commit()


# Viewing expenses
# ----------------

def get_expenses(category, year, month):
    """Single entry point for viewing expenses.
    """
    if category and not (year and month):
        return _get_current_expenses_by_category(category)
    if year and month:
        return _get_expenses_by_month(year, month)
    # Default view is current expenses without a category filter.
    return _get_current_expenses()


def _get_current_expenses():
    """Gets all expenses by current month from database.
    """
    with closing(connection()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute(
                'SELECT ex.cost, cat.name, ex.datetime, ex.comment '\
                '  FROM expense ex '\
                'JOIN category cat ON cat.id = ex.category_fk '\
                'WHERE YEAR(ex.datetime) = YEAR(NOW()) '\
                '  AND MONTH(ex.datetime) = MONTH(NOW()) '\
                'ORDER BY ex.datetime DESC'
            )
            expenses = _expense_objects_from_cursor(cur)
            sum_ = sum([x['cost'] for x in expenses])
            return sum_, expenses


def _get_current_expenses_by_category(category):
    """Gets all expenses by current month and category from database.
    """
    with closing(connection()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute(
                'SELECT ex.cost, cat.name, ex.datetime, ex.comment '\
                '  FROM expense ex ' \
                'JOIN category cat ON cat.id = ex.category_fk '\
                'WHERE YEAR(ex.datetime) = YEAR(NOW()) ' \
                '  AND MONTH(ex.datetime) = MONTH(NOW()) ' \
                '  AND cat.name = "%s"'\
                'ORDER BY ex.datetime DESC' % (category,)
            )
            expenses = _expense_objects_from_cursor(cur)
            sum_ = sum([x['cost'] for x in expenses])
            return sum_, expenses


def _get_expenses_by_month(year, month):
    """Gets all expenses by a given month.
    """
    with closing(connection()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute(
                'SELECT ex.cost, cat.name, ex.datetime, ex.comment '\
                '  FROM expense ex ' \
                'JOIN category cat ON cat.id = ex.category_fk '\
                'WHERE YEAR(ex.datetime) = %s ' \
                '  AND MONTH(ex.datetime) = %s ' \
                'ORDER BY ex.datetime DESC' % (year, month,)
            )
            expenses = _expense_objects_from_cursor(cur)
            sum_ = sum([x['cost'] for x in expenses])
            return sum_, expenses


# Utility functions
# -----------------

def _expense_objects_from_cursor(cur):
    """Returns list of expense objects from database connection cursor.
    """
    expenses = []
    for r in cur.fetchall():
        expenses.append({
            'cost': r[0],
            'category': r[1],
            'datetime': r[2],
            'comment': r[3],
        })
    return expenses


def get_previous_months():
    """Gets all previous months with recorded transactions.
    """
    with closing(connection()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute(
                'SELECT DISTINCT '\
                '  CONCAT(MONTHNAME(datetime), " ", YEAR(datetime)), '\
                '  MONTH(datetime), '\
                '  YEAR(datetime) FROM expense'
            )
            return [{
                'view': c[0],
                'month_num': c[1],
                'year_num': c[2]} for c in cur.fetchall()]
  

def get_categories():
    """Gets all categories from database.
    """
    with closing(connection()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute('SELECT name FROM category')
            categories = [c[0] for c in cur.fetchall()]
            return categories


def connection():
    """Utility function for returning a database connection.
    """
    return MySQLdb.connect(**db_connection_args)

