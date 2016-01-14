"""Represents application user.
"""

import hashlib
import uuid

from slate import db


class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    salt = db.Column(db.String(255))

    def __init__(self, id, name, password, active=True):
        self.id = id
        self.name = name
        hashed, salt = self.hash_password(password)
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

    @classmethod
    def get(cls, username, candidate_pw):
        user = db.session.query(cls).filter(cls.name == username).one()
        if not user:
            return None
        if cls.correct_password(user.password, candidate_pw, user.salt):
            return user
        return None

    @classmethod
    def correct_password(cls, hashed, candidate, salt):
        """Check hashed password.
        """
        return hashlib.sha512(candidate + salt).hexdigest() == hashed

    @classmethod
    def hash_password(cls, password):
        """Hash a password for the first time.
        """
        salt = uuid.uuid4().hex
        hashed = hashlib.sha512(password + salt).hexdigest()
        return hashed, salt
