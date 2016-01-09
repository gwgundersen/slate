"""Configures and starts the web server.
"""


from flask import Flask, session, render_template
from flask.ext.login import LoginManager

from slate.config import config
from slate import db
from slate import endpoints
from slate.user import User


app = Flask(__name__,
            static_url_path='%s/static' % config.get('url', 'base'),
            static_folder='static')

app.secret_key = config.get('cookies', 'secret_key')

# Server endpoints
app.register_blueprint(endpoints.add)
app.register_blueprint(endpoints.auth)
app.register_blueprint(endpoints.expenses)
app.register_blueprint(endpoints.index)

# Login session management
login_manager = LoginManager()
login_manager.init_app(app)


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

