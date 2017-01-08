"""Views reports on expenses.
"""

import datetime

from flask import Blueprint, render_template, request
from flask.ext.login import login_required

from slate import models
from slate.config import config
from slate.models.report import MIN_NUM_REPEATED


reports = Blueprint('reports',
                    __name__,
                    url_prefix='%s/report' % config.get('url', 'base'))


@reports.route('', methods=['GET'])
@login_required
def report_pages():
    """Delegates to functions that build appropriate reports.
    """
    year = request.args.get('year')
    month = request.args.get('month')
    if year:
        year = int(year)
        if month:
            month = int(month)
            return monthly_report(year, month)
        return yearly_report(year)
    else:
        # Default is monthly report for current month/year.
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        return monthly_report(year, month)


def monthly_report(year, month):
    """Build report for month and year.
    """
    report = models.Report(year=year, month=month)
    return render_template('report_monthly.html',
                           report=report)


def yearly_report(year):
    """Build report for entire year.
    """
    report = models.Report(year=year)
    return render_template('report_yearly.html', report=report,
                           MIN_NUM_REPEATED=MIN_NUM_REPEATED)


def _date_handler(date):
    """Formats date for JSON.
    """
    return [date.year, date.month, date.day]
