"""Manages user account page.
"""

from flask import Blueprint, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required, logout_user

from slate import db
from slate.endpoints import viewutils
from slate import models
from slate import dbutils
from slate.config import config
from slate.endpoints import authutils

account = Blueprint('account',
                    __name__,
                    url_prefix='%s/account' % config.get('url', 'base'))


@account.route('/', methods=['GET'])
@login_required
def view_account():
    """View account page.
    """
    auth_message = authutils.auth_message()
    message = request.args.get('message')
    return render_template('account.html',
                           user=current_user,
                           message=message,
                           auth_message=auth_message)


@account.route('/delete', methods=['POST'])
@login_required
def delete_account():
    """Permanently deletes a user and all associated data.
    """
    if current_user.name == 'gwg':
        return 'Greg, use a fake account to test this.'
    id_ = current_user.id
    logout_user()
    models.User.query.filter_by(id=id_).delete()
    db.session.commit()
    return render_template('account-delete-confirmation.html')


@account.route('/update', methods=['POST'])
@login_required
def update_password():
    """Updates a user password.
    """
    old_password = request.form['oldpassword']
    new_password1 = request.form['newpassword1']
    new_password2 = request.form['newpassword2']

    error = None
    if not current_user.is_correct_password(old_password):
        error = 'Old password is incorrect'
    elif new_password1 != new_password2:
        error = 'Passwords do not match'
    elif not new_password1:
        error = 'Password is required'
    elif old_password == new_password1:
        error = 'Password has not changed'

    if error:
        return redirect(url_for('account.view_account',
                                message=error))


    hashed, salt = current_user.hash_password(new_password1)
    current_user.password = hashed
    current_user.salt = salt
    db.session.merge(current_user)
    db.session.commit()
    return redirect(url_for('account.view_account',
                            message='Password was successfully updated'))
