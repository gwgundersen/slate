"""Serves index page.
"""

from flask import Blueprint, render_template
from flask.ext.login import current_user

from slate.config import config


index = Blueprint('index',
                  __name__,
                  url_prefix=config.get('url', 'base'))


@index.route('/', methods=['GET'])
def index_page():
    """Renders index page.
    """
    if current_user.is_anonymous:
        categories = []
    else:
        categories = current_user.categories
    return render_template('index.html',
                           categories=categories)

