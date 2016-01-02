"""Adds an expense.
"""


from flask import Blueprint

from slate.config import config
from slate import db_connection_args


add_api = Blueprint('add_api',
                    __name__,
                    url_prefix='/add')


@add_api.route('/', methods=['GET', 'POST'])
def add():
    import pdb; pdb.set_trace()

