"""Adds an expense.
"""


from flask import Blueprint

from slate.config import config


add_api = Blueprint('index_page',
                    __name__,
                    url_prefix='/%s/add' % config.get('url', 'base'))


@add_api.route('/', methods=['GET', 'POST'])
def add():
    pass

