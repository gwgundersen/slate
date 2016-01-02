"""Serves index page.
"""


from flask import Blueprint, render_template
from flask.ext.login import current_user
import MySQLdb

from slate.config import config


index_page = Blueprint('index_page',
                       __name__,
                       url_prefix=config.get('url', 'base'))


@index_page.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        auth_message = '%s is logged in.' % current_user.name
    else:
        auth_message = 'No user logged in.'
    return render_template('index.html', auth_message=auth_message)

