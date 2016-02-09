"""Handles logins and logouts.
"""

from flask import g
from flask.ext.login import login_user, logout_user, login_required
from sqlalchemy.orm.exc import NoResultFound

from flask import Blueprint, request, redirect, render_template, url_for
from slate.config import config
from slate import app, db, models

auth = Blueprint('auth',
                 __name__,
                 url_prefix=config.get('url', 'base'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form['username']
    password = request.form['password']

    registered_user = models.User.get(username, password)
    if registered_user is None:
        logout_user()
        return render_template('login.html',
                               error='Username or password is invalid')

    app.config.user = registered_user
    login_user(registered_user)
    return redirect(url_for('index.index_page'))


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    g.user = None
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']

    if not username or not username.isalnum():
        return render_template('register.html',
                               error='Username must be alphanumeric')

    password1 = request.form['password1']
    password2 = request.form['password2']

    no_user_by_that_name = False
    try:
        db.session.query(models.User)\
            .filter(models.User.name == username)\
            .one()
    except NoResultFound:
        no_user_by_that_name = True

    if not no_user_by_that_name:
        return render_template('register.html',
                               error='Username already exists')

    if password1 != password2:
        return render_template('register.html',
                               error='Passwords do not match')

    if not password1:
        return render_template('register.html',
                               error='Password is required')

    new_user = models.User(username, password1)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for('index.index_page'))
