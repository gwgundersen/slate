"""Handles logins and logouts.
"""

from flask import g, flash, Blueprint, request, redirect, render_template, \
    url_for
from flask.ext.login import login_user, logout_user, login_required
from sqlalchemy.orm.exc import NoResultFound

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
    login_user(registered_user, remember=True)
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

    username = request.form.get('username')

    if not username or not username.isalnum():
        flash('Username must be alphanumeric.', 'error')
        return render_template('register.html')

    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    try:
        db.session.query(models.User)\
            .filter(models.User.name == username)\
            .one()

        # The line of code above will throw an error if the user does not
        # exist.
        flash('Username already exists.', 'error')
        return redirect(url_for('auth.register'))
    except NoResultFound:
        pass

    if password1 != password2:
        flash('Passwords do not match.', 'error')
        return redirect(url_for('auth.register'))
    if not password1:
        flash('Password is required.', 'error')
        return redirect(url_for('auth.register'))

    new_user = models.User(username, password1)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=True)
    flash('Welcome to Slate!', 'success')
    return redirect(url_for('index.index_page'))
