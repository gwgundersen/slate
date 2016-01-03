"""Configures and starts the web server.
"""


from flask import Flask, render_template
from flask.ext.login import LoginManager
import uuid

from slate.endpoints.auth import auth
from slate.endpoints.add import add
from slate.endpoints.expenses import expenses
from slate.endpoints.index import index
from slate.config import config
from slate import db
from slate.user import User


app = Flask(__name__,
            static_url_path='%s/static' % config.get('url', 'base'),
            static_folder='static')

app.secret_key = uuid.uuid4().hex

# Server endpoints
app.register_blueprint(add)
app.register_blueprint(auth)
app.register_blueprint(expenses)
app.register_blueprint(index)

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
    return render_template('404.html')

