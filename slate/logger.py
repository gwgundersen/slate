"""Logs messages to file, rotating after a certain number of messages.
"""


import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('info.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)

