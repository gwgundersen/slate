"""Represents application user.
"""

import datetime

from sqlalchemy.orm.exc import NoResultFound

from slate import db, crypto
from slate.models import Category, Expense


class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    salt = db.Column(db.String(255))
    _expenses = db.relationship('Expense', backref=db.backref('user'))
    categories = db.relationship('Category', backref=db.backref('user'))
    email = db.Column(db.String(255))
    password_reset_token = db.Column(db.String(255))
    password_reset_expiration = db.Column(db.Date)

    def __init__(self, name, password, active=True):
        self.name = name
        hashed, salt = crypto.salt_and_hash_password(password)
        self.password = hashed
        self.salt = salt

        categories = []
        default_categories = ['alcohol',
                              'bills',
                              'clothing',
                              'entertainment',
                              'food (in)',
                              'food (out)',
                              'household',
                              'medical',
                              'miscellaneous',
                              'rent/mortgage',
                              'transportation',
                              'travel/vacation']
        for name in default_categories:
            categories.append(
                Category(name)
            )

        self.categories = categories
        self.active = active

    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    def expenses(self, category=None, year=None, month=None):
        """Returns list of expenses. If category is provided, filters by
        category. If year and month are provided, filters by year and month.
        """
        query = db.session.query(Expense)\
            .filter(Expense.user_fk == self.id)
        if category:
            query = query\
                .join(Category)\
                .filter(Category.id == category.id)
        if year:
            query = query\
                .filter(db.extract('year', Expense.date_time) == int(year))
            if month:
                query = query\
                    .filter(db.extract('month', Expense.date_time) == int(month))
        else:
            now = datetime.datetime.now()
            query = query\
                .filter(db.extract('year', Expense.date_time) == now.year)\
                .filter(db.extract('month', Expense.date_time) == now.month)
        return query\
            .order_by(Expense.date_time.desc())\
            .all()

    def all_expenses(self):
        """Returns list of expenses. If category is provided, filters by
        category. If year and month are provided, filters by year and month.
        """
        return db.session.query(Expense)\
            .filter(Expense.user_fk == self.id)\
            .order_by(Expense.date_time.desc())\
            .all()

    @classmethod
    def get(cls, username, candidate_pw):
        """Returns user by name if they exist and the provided password is
        correct. Returns None otherwise.
        """
        try:
            user = db.session.query(cls).filter(cls.name == username).one()
        except NoResultFound:
            return None
        if user.is_correct_password(candidate_pw):
            return user
        return None

    def is_correct_password(self, candidate):
        """Returns True if the candidate password is correct, False otherwise.
        """
        return crypto.is_correct_password(self.password, candidate, self.salt)

    def already_has_category(self, new_name):
        """Returns True if user already has category by that name, False
        otherwise.
        """
        for category in self.categories:
            if category.name == new_name:
                return True
        return False
