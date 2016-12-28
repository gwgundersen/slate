"""Handles logins and logouts.
"""

from flask import g, flash, Blueprint, request, redirect, render_template, \
    url_for
from flask.ext.login import login_user, logout_user, login_required
import datetime

from slate.config import config
from slate import app, db, models, email, crypto

auth = Blueprint('auth',
                 __name__,
                 url_prefix=config.get('url', 'base'))

TOKEN_TIMEOUT = 30


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form['username']
    password = request.form['password']

    registered_user = models.User.get(username, password)
    if not registered_user:
        logout_user()
        flash('Username or password is invalid', 'error')
        return render_template('login.html')

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

    user = db.session.query(models.User)\
        .filter(models.User.name == username)\
        .one_or_none()

    if user:
        flash('Username already exists.', 'error')
        return redirect(url_for('auth.register'))

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


@auth.route('/reset', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'GET':
        return render_template('reset_request.html', timeout=TOKEN_TIMEOUT)

    username = request.form['username']
    address = request.form['email']

    user = db.session.query(models.User)\
        .filter(models.User.name == username)\
        .one_or_none()

    if not user or address != user.email:
       flash('Username or email address is incorrect.', 'error')
       return render_template('reset_request.html', timeout=TOKEN_TIMEOUT)

    token = crypto.generate_nonce()
    user.password_reset_token = token
    expiration = datetime.datetime.now() + \
                 datetime.timedelta(minutes=TOKEN_TIMEOUT)
    user.password_reset_expiration = expiration
    db.session.merge(user)
    db.session.commit()

    is_debug = config.getboolean('mode', 'debug')
    base = 'http://localhost:8080' if is_debug else 'http://gregorygundersen.com'
    url = '%s/slate/reset/%s' % (base, token)
    email.send(url, 'Reset your Slate password', address)

    flash('An email was sent to %s.' % address, 'Success')
    return redirect(url_for('index.index_page'))


@auth.route('/reset/<string:token>',  methods=['GET', 'POST'])
def reset_form(token):
    if request.method == 'GET':
        return render_template('reset_form.html', token=token)

    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    user = db.session.query(models.User)\
        .filter(models.User.name == username)\
        .one_or_none()

    early_exit_url = redirect(url_for('auth.reset_form', token=token))
    if not user:
        flash('Invalid username.', 'error')
        return early_exit_url
    if user.password_reset_token != token:
        flash('Invalid password reset token.', 'error')
        return early_exit_url
    if password1 != password2:
        flash('Passwords do not match.', 'error')
        return early_exit_url
    if not password1:
        flash('Password is required.', 'error')
        return early_exit_url

    # Verify token is not expired.
    now = datetime.datetime.now()
    if user.password_reset_expiration < now:
        flash('Password reset token has expired.', 'error')
        return redirect(url_for('auth.reset_request'))

    # Hash, salt, and save new password.
    hashed, salt = crypto.salt_and_hash_password(password1)
    user.password = hashed
    user.salt = salt

    # The user should not be able to use the link more than once.
    user.password_reset_token = None
    user.password_reset_expiration = None

    db.session.merge(user)
    db.session.commit()

    # Log user into application.
    app.config.user = user
    login_user(user, remember=True)
    flash('Password was reset.', 'success')
    return redirect(url_for('index.index_page'))
