"""Serves index page.
"""


from flask import Blueprint, render_template
from flask.ext.login import current_user
import MySQLdb

from slate import db
from slate.config import config


index = Blueprint('index',
                  __name__,
                  url_prefix=config.get('url', 'base'))


@index.route('/', methods=['GET'])
def index_page():
    categories = db.get_categories()
    if current_user.is_authenticated:
        auth_message = '%s is logged in.' % current_user.name
    else:
        auth_message = 'No user logged in.'
    return render_template('index.html',
                           categories=categories,
                           auth_message=auth_message)

