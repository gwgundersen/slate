"""Utility functions for user authentication."""

import hashlib
import random
import uuid


def generate_nonce():
    """Generate pseudorandom number.
    """
    return str(random.SystemRandom().randint(0, 100000000))


def salt_and_hash_password(password, salt=None):
    """Salt and hash password.
    """
    if not salt:
        salt = uuid.uuid4().hex
    hashed = hashlib.sha512(password + salt).hexdigest()
    return hashed, salt


def is_correct_password(hashed, candidate, salt):
    """Returns True if the candidate password is correct, False otherwise.
    """
    answer, salt = salt_and_hash_password(candidate, salt)
    return hashed == answer
