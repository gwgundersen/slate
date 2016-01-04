"""Configures and starts the web server.
"""


from flask import Flask, session, render_template
from flask.ext.login import LoginManager
import logging
from logging.handlers import RotatingFileHandler

from slate.config import config
from slate import db
from slate.user import User


handler = RotatingFileHandler('info.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)


app = Flask(__name__,
            static_url_path='%s/static' % config.get('url', 'base'),
            static_folder='static')

app.secret_key = 'Section.80'

# Logging
#if app.debug:
app.logger.addHandler(handler)

# Server endpoints
# Import endpoints after configuring logger to avoid circular imports
from slate import endpoints
app.register_blueprint(endpoints.add)
app.register_blueprint(endpoints.auth)
app.register_blueprint(endpoints.expenses)
app.register_blueprint(endpoints.index)

# Login session management
login_manager = LoginManager()
login_manager.init_app(app)

app.logger.info('BEGIN Application has started')


@login_manager.user_loader
def load_user(user_id):
    tpl = db.get_user_by_id(user_id)
    return User(user_id, tpl[1], tpl[2])


login_manager.login_view = 'auth.login'


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

