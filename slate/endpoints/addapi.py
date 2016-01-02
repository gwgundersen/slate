"""Adds an expense.
"""


from flask import Blueprint, request, render_template
from flask.ext.login import current_user, login_required
import datetime

from slate import db
from slate.config import config


add_api = Blueprint('add_api',
                    __name__,
                    url_prefix='%s/add' % config.get('url', 'base'))


@add_api.route('', methods=['POST'])
@login_required
def add():
    """Adds expense.
    """
    if not current_user.is_authenticated():
        message = 'Please log in.'
        return render_template('index',
                               message=message)
    import pdb; pdb.set_trace()
    cost = request.form.get('cost')
    category = request.form.get('category')
    comment = request.form.get('comment')
    datetime_ = datetime.datetime.now()
    db.save_expense(cost, category, datetime_, comment)
    return 'success'

