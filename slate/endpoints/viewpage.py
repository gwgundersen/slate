"""Views expenses.
"""


from flask import Blueprint, render_template
import MySQLdb

from slate.config import config, db_connection_args


view_page = Blueprint('view_page',
                      __name__,
                      url_prefix='/view')


@view_page.route('/', methods=['GET'])
def view_default():
    """Views expenses by current month.
    """
    conn = MySQLdb.connect(**db_connection_args)
    try:
        cur = conn.cursor()
        cur.execute('''
            SELECT ex.cost, cat.name, ex.datetime, ex.comment
            FROM expense ex
              JOIN category cat ON cat.id = ex.category_fk
            WHERE YEAR(ex.datetime) = YEAR(NOW())
              AND MONTH(ex.datetime) = MONTH(NOW())
        ''')

        expenses = []
        for r in cur.fetchall():
            expenses.append({
                'cost': r[0],
                'category': r[1],
                'datetime': r[2],
                'comment': r[3],
            })

        cur.execute('SELECT name FROM category')
        categories = [c[0] for c in cur.fetchall()]

        cur.close()
        return render_template('view.html',
                               categories=categories,
                               expenses=expenses)
    except Exception as e:
        print(e)
    finally:
        conn.close()


@view_page.route('/<category>', methods=['GET'])
def view_by_category(category):
    conn = MySQLdb.connect(**db_connection_args)
    try:
        cur = conn.cursor()
        sql = '' \
            'SELECT ex.cost, cat.name, ex.datetime, ex.comment ' \
            'FROM expense ex ' \
            '  JOIN category cat ON cat.id = ex.category_fk ' \
            'WHERE YEAR(ex.datetime) = YEAR(NOW()) ' \
            '  AND MONTH(ex.datetime) = MONTH(NOW()) ' \
            '  AND cat.name = "%s"' % category
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

        cur.execute('SELECT name FROM category')
        categories = [c[0] for c in cur.fetchall()]

        cur.close()
        return render_template('view.html',
                               categories=categories,
                               expenses=expenses)
    except Exception as e:
        print(e)
    finally:
        conn.close()

