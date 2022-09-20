# Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required, current_user

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.commons.display_context import display_context
from tracking.groups.group_models import find_group_by_id

group_bp = Blueprint(
    'group_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@group_bp.route('/create', methods=['POST', 'GET'])
@login_required
def group_create():
    if not current_user.can_create_group:
        return redirect_hacks()
    form = group_create_form()
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(url_for('group_bp.list'))
    if form.validate_on_submit():
        group = create_group_from_form(current_user, form)
        return redirect(url_for('group_bp.group_view', group_id=group.id))
    else:
        return render_template('group_create_form.j2', form=form, tab="group", **display_context())


def group_create_form():
    pass


def create_group_from_form(current_user, form):
    pass


@group_bp.route('/delete/<int:group_id>')
@login_required
def group_delete(group_id):
    group = find_group_by_id(group_id)
    if group is not None and group.user_may_delete(current_user):
        database.session.delete(group)
        database.session.commit()
        return redirect(url_for('group_bp.group_list'))
    else:
        return redirect_hacks()


@group_bp.route('/list')
@login_required
def group_list():
    render_template('group_list.j2', tab="group")


@group_bp.route('/update/<int:group_id>', methods=['GET', 'POST'])
@login_required
def group_update(group_id):
    group = find_group_by_id(group_id)
    if group and group.user_can_update(current_user):
        form = group_update_form(group)
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('group_bp.group_view', group_id=group_id))
        if form.validate_on_submit():
            update_group_from_form(group, form)
            database.session.commit()
            return redirect(url_for('group_bp.group_view', group_id=group.id))
        else:
            return render_template('group_edit_form.j2', form=form, tab="group", **display_context())
    else:
        return redirect_hacks()


def group_update_form(group):
    pass


def update_group_from_form(group, form):
    form.populate_obj(group)


@group_bp.route('/view/<int:group_id>')
@login_required
def group_view(group_id):
    group = find_group_by_id(group_id)
    if group is not None and group.user_may_view(current_user):
        return render_template('group_view.j2', group=group, tab="group", **display_context())
    else:
        return redirect(url_for('home_bp.home'))
