"""Handles user representation and password encryption.
"""


import bcrypt

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
        id_, username, hashed_password = tpl
        if cls.correct_password(plain_password, hashed_password):
            return cls(id_, username)
        return None

    @classmethod
    def correct_password(cls, plain_text_password, hashed_password):
        """Check hashed password.
        """
        # Using bcrypt, the salt is saved into the hash itself.
        return bcrypt.checkpw(plain_text_password, hashed_password)

    @classmethod
    def hash_password(cls, plain_text_password):
        """Hash a password for the first time.
        """
        # Using bcrypt, the salt is saved into the hash itself.
        return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

