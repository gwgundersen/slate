"""Handles logins and logouts.
"""


from flask import Blueprint, request, redirect, render_template, url_for
from flask.ext.login import login_user, logout_user, login_required

from slate.user import User
from slate.config import config


auth = Blueprint('auth',
                 __name__,
                 url_prefix=config.get('url', 'base'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.get(username, password)
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        logout_user()
        return render_template('login.html',
                               message='Incorrect credentials.')

    login_user(registered_user)
    
    # TODO: The 'next' argument is not being detected by Flask. Why?
    #next_ = request.args.get('next')
    #return redirect(next_ or url_for('index.index_page'))
    
    return redirect(url_for('index.index_page'))


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.index_page'))

