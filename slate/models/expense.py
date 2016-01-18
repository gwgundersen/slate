"""Represents a financial expense.
"""

import datetime

from slate import db


class Expense(db.Model):

    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float)
    date_time = db.Column(db.Date)
    comment = db.Column(db.String(255))
    category_fk = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_fk = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, cost, category, comment, user):
        self.cost = cost
        self.category = category
        self.date_time = datetime.datetime.now()
        self.comment = comment
        self.user = user

    @property
    def serialize(self):
        return {
            'cost': self.cost,
            'category': self.category.name,
            'date_time': str(self.date_time),
            'comment': self.comment
        }
