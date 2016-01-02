"""Configures and starts the web server.
"""


from flask import Flask

from slate.endpoints.indexpage import index_page
from slate.config import config


app = Flask(__name__, static_url_path='/slate/static', static_folder='static')
app.register_blueprint(index_page)


