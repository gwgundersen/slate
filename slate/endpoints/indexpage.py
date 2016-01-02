"""Serves index page.
"""


from flask import Blueprint, render_template
import MySQLdb

from slate.config import config


index_page = Blueprint('index_page',
                       __name__,
                       url_prefix='/%s' % config.get('url', 'base'))


@index_page.route('/', methods=['GET'])
def index():
    """
    db_connection_args = {
        'user': config.get('db', 'user'),
        'passwd': config.get('db', 'passwd'),
        'db': config.get('db', 'db'),
        'host': config.get('db', 'host')
    }
    try:
        conn = MySQLdb.connect(**db_connection_args)
        cur = conn.cursor()
        cur.execute('SELECT * FROM expense')
        return str(cur.fetchall())
    except Exception as e:
        print(e)
    finally:
        conn.close()
    """
    return render_template('index.html')

