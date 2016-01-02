"""Handles all database transactions.
"""


def get():
    from slate import mysql
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM expense')
    return str(cur.fetchall())

