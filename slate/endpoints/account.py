"""Manages user account page.
"""

import calendar
import os
import StringIO
import zipfile

from flask import Blueprint, redirect, Response, render_template, request, url_for
from flask.ext.login import current_user, login_required, logout_user

from slate import db, dbutils, models
from slate.config import config

account = Blueprint('account',
                    __name__,
                    url_prefix='%s/account' % config.get('url', 'base'))


@account.route('/', methods=['GET'])
@login_required
def view_account():
    """View account page.
    """
    message = request.args.get('message')
    return render_template('account.html',
                           message=message)


@account.route('/settings', methods=['GET'])
@login_required
def view_settings():
    """View account settings page.
    """
    message = request.args.get('message')
    return render_template('settings.html')


@account.route('/download', methods=['GET'])
@login_required
def download_data():
    """Returns a zip file of CSV files, one for every month.
    """
    filenames = _write_files_and_return_names()
    zip_subdir = 'slate'
    zip_filename = '%s.zip' % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        # Add file, at correct path
        zf.write(fpath, zip_path)

    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = Response(s.getvalue(), mimetype='application/x-zip-compressed')
    content_disposition = 'attachment; filename=%s' % zip_filename
    resp.headers['Content-Disposition'] = content_disposition

    # Delete files from server before sending them over the wire.
    for f in filenames:
        os.remove(f)

    return resp


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


def _write_files_and_return_names():
    """Writes CSV file with expenses for each monnth; returns all filenames.
    """
    files = []
    months = dbutils.get_all_months()
    for d in months:
        year = d['year_num']
        month = d['month_num']
        month_name = calendar.month_name[int(month)]
        expenses = current_user.expenses(year=year, month=month)
        filename = 'slate/static/downloads/%s %s.tsv' % (year, month_name)
        with open(filename, 'w+') as f:
            header = 'cost\tcomment\tcategory\tdiscretionary\ttime\n'
            f.write(header)
            for e in expenses:
                line = [str(e.cost), e.comment, e.category.name,
                        str(e.discretionary), str(e.date_time)]
                line = '\t'.join(line) + '\n'
                f.write(line)
        files.append(filename)
    return files
