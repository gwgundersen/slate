"""Serves index page.
"""


from flask import Blueprint, render_template

from slate.config import config


index_page = Blueprint('index_page',
                       __name__,
                       url_prefix='/%s' % config.get('url', 'base'))


@index_page.route('/', methods=['GET'])
def index():
    r = db.session.query('SELECT * FROM expense')
    import pdb; pdb.set_trace()
    return render_template('index.html')

