"""Configures and starts the web server.
"""

from flask import Flask, g, session as flask_session, render_template
from flask.ext.login import LoginManager, current_user, user_logged_out

from flask.ext.sqlalchemy import SQLAlchemy

from slate.config import config


app = Flask(__name__,
            static_url_path='%s/static' % config.get('url', 'base'),
            static_folder='static')


# Database connection
# ----------------------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:3306/%s' % (
    config.get('db', 'user'),
    config.get('db', 'passwd'),
    config.get('db', 'host'),
    config.get('db', 'db')
)
app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800 # Recycle every 30 min.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)


if config.getboolean('mode', 'debug'):
    # Add a trailing slash, so the base tag URL will be "/slate/"
    app.config.base_tag_url = '%s/' % config.get('url', 'base')
else:
    # Manually set the base tag URL to "/slate/". Why can't we use the config
    # value? Because in production, the application runs on the server in the
    # `slate` directory. To the application in production, "/" is this
    # directory, so "/slate" would result in a URL mapping to "/slate/slate".
    # Yes, this is annoying.
    app.config.base_tag_url = '/slate/'


# Server endpoints
# ----------------------------------------------------------------------------
from slate import endpoints
app.register_blueprint(endpoints.account)
app.register_blueprint(endpoints.auth)
app.register_blueprint(endpoints.categories)
app.register_blueprint(endpoints.expenses)
app.register_blueprint(endpoints.index)
app.register_blueprint(endpoints.reports)


# Login session management
# ----------------------------------------------------------------------------
# Change this key to force all users to re-authenticate.
app.secret_key = config.get('cookies', 'secret_key')
# Limit "remember me" cookie to path. Default is "/".
app.config['REMEMBER_COOKIE_PATH'] = '/slate'

from slate import models
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@app.before_request
def before_request():
    """
    """
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    """
    """
    user = db.session.query(models.User).get(user_id)
    return user


# @user_logged_out.connect_via(app)
# def unset_current_user(sender, user):
#     """When the user logs out, we need to unset this global variable.
#     """
#     print('logging user out')
#     app.config.user = None


@app.before_request
def make_session_permanent():
    """Sets Flask session to 'permanent', meaning 31 days.
    """
    flask_session.permanent = True


# Error handling
# ----------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    """Handles all 404 requests.
    """
    return render_template('404.html')

