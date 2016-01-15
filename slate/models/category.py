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

    def __init__(self, name):
        self.name = name
