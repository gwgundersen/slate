"""Configures and starts the web server.
"""

from flask import Flask, session, render_template
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

from slate.config import config
#from slate import models


app = Flask(__name__,
            static_url_path='%s/static' % config.get('url', 'base'),
            static_folder='static')

app.secret_key = config.get('cookies', 'secret_key')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:3306/%s' % (
    config.get('db', 'user'),
    config.get('db', 'passwd'),
    config.get('db', 'host'),
    config.get('db', 'db')
)
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

# Server endpoints
from slate import endpoints
app.register_blueprint(endpoints.auth)
app.register_blueprint(endpoints.expenses)
app.register_blueprint(endpoints.index)

# Login session management
from slate import models
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).get(user_id)


@app.errorhandler(404)
def page_not_found(e):
    """Handles all 404 requests.
    """
    return render_template('404.html')


@app.before_request
def make_session_permanent():
    """Sets Flask session to 'permanent', meaning 31 days.
    """
    session.permanent = True

