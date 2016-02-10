"""Manages category endpoints.
"""

from flask import Blueprint, flash, redirect, render_template, request, \
    url_for
from flask.ext.login import current_user, login_required

from slate import db
from slate import models
from slate.config import config


categories = Blueprint('categories',
                       __name__,
                       url_prefix='%s/categories' % config.get('url', 'base'))


@categories.route('/add', methods=['POST'])
@login_required
def add_category():
    """Adds category if not duplicate name for user.
    """
    new_name = request.form.get('name')
    if current_user.already_has_category(new_name):
        flash('Category by that name already exists!', 'error')
        return redirect(url_for('account.view_settings'))

    category = models.Category(new_name)
    current_user.categories.append(category)
    db.session.merge(current_user)
    db.session.commit()
    flash('New category successfully created.', 'success')
    return redirect(url_for('account.view_settings'))


@categories.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_category():
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
        new_name = request.form.get('name', '').lower()

        if current_user.already_has_category(new_name):
            flash('Category by that name already exists!', 'error')
            return redirect(url_for('categories.edit_category', id=id_))

        category.name = new_name
        db.session.merge(category)
        db.session.commit()
        flash('Category successfully renamed.', 'success')
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
    flash('Category successfully deleted.', 'success')
    return redirect(url_for('account.view_settings'))
