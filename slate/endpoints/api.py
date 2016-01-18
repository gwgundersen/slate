"""Handles logins and logouts.
"""

from flask import Blueprint, jsonify, request
from flask.ext.login import current_user

from slate.config import config
from slate import dbutils

api = Blueprint('api',
                __name__,
                url_prefix='%s/api' % config.get('url', 'base'))


@api.route('/expenses/<username>', methods=['GET'])
def get_expense(username):
    year = request.args.get('year')
    month = request.args.get('month')
    if year and month:
        year = int(year)
        month = int(month)
        expenses = dbutils.get_category_subtotals(username, year, month)
    else:
        expenses = dbutils.get_category_subtotals(username)
    return jsonify({
        'expenses': expenses
    })