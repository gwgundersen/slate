"""Handles logins and logouts.
"""

from flask import Blueprint, jsonify, request
from slate.config import config
from slate import dbutils

api = Blueprint('api',
                __name__,
                url_prefix='%s/api' % config.get('url', 'base'))


@api.route('/expenses', methods=['GET'])
def get_expense():
    year = request.args.get('year')
    month = request.args.get('month')
    if year and month:
        year = int(year)
        month = int(month)
        expenses = dbutils.get_expense_totals_by_category(year, month)
    else:
        expenses = dbutils.get_expense_totals_by_category()
    return jsonify({
        'expenses': expenses
    })