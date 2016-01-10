"""Serves index page.
"""


from flask import Blueprint, render_template, request
from flask.ext.login import current_user

from slate import db
from slate.config import config
from slate.endpoints import authutils


index = Blueprint('index',
                  __name__,
                  url_prefix=config.get('url', 'base'))


@index.route('/', methods=['GET'])
def index_page():
    categories = db.get_categories()
    error = request.args.get('error')
    auth_message = authutils.auth_message()
    return render_template('index.html',
                           categories=categories,
                           error=error,
                           auth_message=auth_message)

