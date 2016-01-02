"""Configures and starts the web server.
"""


from flask import Flask, render_template
from flask.ext.login import LoginManager

from slate.endpoints.authapi import auth_api
from slate.endpoints.addapi import add_api
from slate.endpoints.indexpage import index_page
from slate.endpoints.viewpage import view_page
from slate.config import config
from slate import db
from slate.user import User


BASE = '%s/static' % config.get('url', 'base')
print(BASE)
app = Flask(__name__,
            static_url_path=BASE,
            static_folder='static')

# Server endpoints
app.register_blueprint(add_api)
app.register_blueprint(auth_api)
app.register_blueprint(index_page)
app.register_blueprint(view_page)

# Login session management
app.secret_key = 'many random bytes'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    tpl = db.get_user_by_id(user_id)
    return User(user_id, tpl[1], tpl[2])


login_manager.login_view = 'auth_api.login'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

