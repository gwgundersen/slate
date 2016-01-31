"""Serves index page.
"""

from flask import Blueprint, render_template, request

from slate.config import config
from slate import dbutils


index = Blueprint('index',
                  __name__,
                  url_prefix=config.get('url', 'base'))


@index.route('/', methods=['GET'])
def index_page():
    """Renders index page.
    """
    categories = dbutils.get_categories()
    error = request.args.get('error')
    return render_template('index.html',
                           categories=categories,
                           error=error)

