"""Utility functions for authentication that are independent of endpoints.
"""


from flask.ext.login import current_user


def auth_message():
    """Returns the correct authentication message for all views.
    """
    if current_user.is_authenticated:
        return '%s is logged in.' % current_user.name
    else:
        return 'No user logged in.'