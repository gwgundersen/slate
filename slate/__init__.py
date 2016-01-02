"""Configures and starts the web server.
"""


from flask import Flask
import MySQLdb

from slate.endpoints.indexpage import index_page
from slate.config import config


app = Flask(__name__, static_url_path='/slate/static', static_folder='static')

mode = config.get('general', 'mode')

# Database configuration
db = MySQLdb.connect(host='localhost',
                     user=config.get('db', 'user'),
                     passwd=config.get('db', 'passwd'),
                     db=config.get('db', 'db'))

cur = db.cursor()
cur.execute("SELECT * FROM expense")

# Server endpoints
app.register_blueprint(index_page)

