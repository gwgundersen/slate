"""Represents application user.
"""

import datetime
import hashlib
import uuid

from sqlalchemy.orm.exc import NoResultFound

from slate import db
from slate.models import Category, Expense


class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    salt = db.Column(db.String(255))
    _expenses = db.relationship('Expense', backref=db.backref('user'))

    def __init__(self, name, password, active=True):
        self.name = name
        hashed, salt = User.hash_password(password)
        self.password = hashed
        self.salt = salt
        self.active = active

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    def expenses(self, category=None, year=None, month=None):
        query = db.session.query(Expense)\
            .join(User)\
            .filter(User.name == self.name)
        if category:
            query = query\
                .join(Category)\
                .filter(Category.name == category.lower())
        if year and month:
            query = query\
                .filter(db.extract('year', Expense.date_time) == int(year))\
                .filter(db.extract('month', Expense.date_time) == int(month))
        else:
            now = datetime.datetime.now()
            query = query\
                .filter(db.extract('year', Expense.date_time) == now.year)\
                .filter(db.extract('month', Expense.date_time) == now.month)
        return query\
            .order_by(Expense.date_time.desc())\
            .all()

    @classmethod
    def get(cls, username, candidate_pw):
        try:
            user = db.session.query(cls).filter(cls.name == username).one()
        except NoResultFound:
            return None
        if User._is_correct_password(user.password, candidate_pw, user.salt):
            return user
        return None

    @staticmethod
    def _is_correct_password(hashed, candidate, salt):
        """Returns True if the candidate password is correct, False otherwise.
        """
        return hashlib.sha512(candidate + salt).hexdigest() == hashed

    def is_correct_password(self, candidate):
        """Returns True if the candidate password is correct, False otherwise.
        """
        return self._is_correct_password(self.password, candidate, self.salt)

    @staticmethod
    def hash_password(password):
        """Hash a password for the first time.
        """
        salt = uuid.uuid4().hex
        hashed = hashlib.sha512(password + salt).hexdigest()
        return hashed, salt
