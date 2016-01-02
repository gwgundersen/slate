"""Serves index page.
"""


from flask import Blueprint

from slate.config import config


index_page = Blueprint('index_page',
                       __name__,
                       url_prefix='/%s' % config.get('url', 'base'))


@index_page.route('/', methods=['GET'])
def index():
    return 'Hello World!'

