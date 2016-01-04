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
    """Gets all expenses by current month from database.
    """
    conn = connection()
    with closing(connection()) as conn:
        with closing(conn.cursor()) as cur:
            sql = ''\
                  'SELECT ex.cost, cat.name, ex.datetime, ex.comment '\
                  'FROM expense ex '\
                  '  JOIN category cat ON cat.id = ex.category_fk '

            if category:
                sql += 'WHERE cat.name = "%s" AND ' % category
            else:
                sql += 'WHERE '

            # The AND or WHERE is handled above.
            if year and month:
                sql += 'YEAR(ex.datetime) = %s '\
                       '  AND MONTH(ex.datetime) = %s ' % (
                           year, month
                       )
            else:
                sql += 'YEAR(ex.datetime) = YEAR(NOW()) '\
                       '  AND MONTH(ex.datetime) = MONTH(NOW()) '

            sql += 'ORDER BY ex.datetime DESC '
            print(sql)
            cur.execute(sql)

            expenses = []
            for r in cur.fetchall():
                expenses.append({
                    'cost': r[0],
                    'category': r[1],
                    'datetime': r[2],
                    'comment': r[3],
                })

            sum_ = sum([x['cost'] for x in expenses])

            return sum_, expenses


def get_expenses_by_category(category):
    """Gets all expenses by current month and category from database.
    """
    with closing(connection()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute(''\
                'SELECT ex.cost, cat.name, ex.datetime, ex.comment '\
                'FROM expense ex ' \
                '  JOIN category cat ON cat.id = ex.category_fk '\
                'WHERE YEAR(ex.datetime) = YEAR(NOW()) ' \
                '  AND MONTH(ex.datetime) = MONTH(NOW()) ' \
                '  AND cat.name = "%s"'\
                'ORDER BY ex.datetime DESC' % category
            )

            expenses = []
            for r in cur.fetchall():
                expenses.append({
                    'cost': r[0],
                    'category': r[1],
                    'datetime': r[2],
                    'comment': r[3],
                })

            cur.execute(''\
                'SELECT SUM(ex.cost) '\
                'FROM expense ex '\
                '  JOIN category cat ON cat.id = ex.category_fk '\
                'WHERE YEAR(ex.datetime) = YEAR(NOW()) ' \
                '  AND MONTH(ex.datetime) = MONTH(NOW()) ' \
                '  AND cat.name = "%s"' % category)

            sum_ = sum([x['cost'] for x in expenses])

            return sum_, expenses


# Utility functions
# -----------------

def get_month_years():
    """Gets all distinct month-year combinations.
    """
    with closing(connection()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute(
                'SELECT DISTINCT CONCAT(MONTHNAME(datetime), " ", '\
                'YEAR(datetime)) FROM expense'
            )
            year_months = [c[0] for c in cur.fetchall()]
            return year_months
  

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

