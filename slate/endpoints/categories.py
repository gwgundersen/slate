"""Manages category endpoints.
"""

from flask import Blueprint, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required

from slate import db
from slate.endpoints import viewutils
from slate import models
from slate import dbutils
from slate.config import config


categories = Blueprint('categories',
                       __name__,
                       url_prefix='%s/categories' % config.get('url', 'base'))


# Add, edit, delete
# ----------------------------------------------------------------------------

@categories.route('/add', methods=['POST'])
@login_required
def add_category():
    """Adds category.
    """
    # TODO: Validation: shouldn't be an existing category name for user.
    category_name = request.args.get('category')
    category = models.Category(category_name)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('expenses.expenses_default'))


@categories.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_expense():
    """Edits user category.
    """
    if request.method == 'GET':
        id_ = request.args.get('id')
        category = db.session.query(models.Category).get(id_)
        return render_template('category-edit.html',
                               category=category)
    else:
        id_ = request.form.get('id')
        category = db.session.query(models.Category).get(id_)
        category.name = request.form.get('name')
        db.session.merge(category)
        db.session.commit()
        return redirect(url_for('account.view_settings'))


@categories.route('/delete', methods=['POST'])
@login_required
def delete_category():
    """Deletes category and all related expenses.
    """
    id_ = request.form.to_dict()['id']
    category = db.session.query(models.Category).get(id_)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('expenses.expenses_default'))
