"""Handles application-wide configurations.
"""


from ConfigParser import ConfigParser


config = ConfigParser()
config.read('slate/config.ini')

