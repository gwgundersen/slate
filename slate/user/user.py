"""Handles user representation and password encryption.
"""


import hashlib, uuid

from slate import db


class User(object):

    def __init__(self, id_, name, active=True):
        self.id_ = id_
        self.name = name
        self.active = active

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id_

    @classmethod
    def get(cls, username, plain_password):
        tpl = db.get_user(username)
        if tpl is None:
            return None
        id_, username, hashed_password, salt = tpl
        if cls.correct_password(plain_password, hashed_password, salt):
            return cls(id_, username)
        return None

    @classmethod
    def correct_password(cls, plain_text, hashed, salt):
        """Check hashed password.
        """
        return hashlib.sha512(plain_text + salt).hexdigest() == hashed

    @classmethod
    def hash_password(cls, password):
        """Hash a password for the first time.
        """
        salt = uuid.uuid4().hex
        hashed = hashlib.sha512(password + salt).hexdigest()
        return hashed, salt

