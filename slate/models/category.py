"""An expense category.
"""

import datetime

from slate import db
from slate.models.expense import Expense


class Category(db.Model):

    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    expenses = db.relationship('Expense', backref=db.backref('category'))
    user_fk = db.Column(db.Integer, db.ForeignKey('user.id'))
    hide_in_report = db.Column(db.Boolean)

    def __init__(self, name, hide_in_report):
        self.name = name
        self.hide_in_report = hide_in_report
