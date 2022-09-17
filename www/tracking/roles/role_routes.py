#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, url_for, redirect, render_template
from flask_login import login_required, current_user

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.roles.role_forms import RoleCreateForm, RoleUpdateForm
from tracking.roles.role_models import find_role_by_id

role_bp = Blueprint(
    'role_bp', __name__,
    template_folder='../templates',
    static_folder='static',
)


@role_bp.route('/create', methods=['POST', 'GET'])
@login_required
def role_create():
    if not current_user.can_create_role:
        return redirect_hacks()
    form = role_create_form()
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(url_for('role_bp.list'))
    if form.validate_on_submit():
        role = create_role_from_form(current_user, form)
        return redirect(url_for('role_bp.role_view', role_id=role.id))
    else:
        return render_template('role_create_form.j2', form=form, tab="role")


def role_create_form():
    return RoleCreateForm()


def create_role_from_form(current_user, form):
    pass


@role_bp.route('/delete/<int:role_id>')
@login_required
def role_delete(role_id):
    role = find_role_by_id(role_id)
    if role is not None and role.user_may_delete(current_user):
        database.session.delete(role)
        database.session.commit()
        return redirect(url_for('role_bp.role_list'))
    else:
        return redirect_hacks()


@role_bp.route('/list')
@login_required
def role_list():
    render_template('role_list.j2', tab="role")


@role_bp.route('/update/<int:role_id>', methods=['GET', 'POST'])
@login_required
def role_update(role_id):
    role = find_role_by_id(role_id)
    if role and role.user_can_update(current_user):
        form = role_update_form(role)
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('role_bp.role_view', role_id=role_id))
        if form.validate_on_submit():
            update_role_from_form(role, form)
            database.session.commit()
            return redirect(url_for('role_bp.role_view', role_id=role.id))
        else:
            return render_template('role_edit_form.j2', form=form, tab="role")
    else:
        return redirect_hacks()


def role_update_form(role):
    RoleUpdateForm(role)


def update_role_from_form(role, form):
    form.populate_obj(role)


@role_bp.route('/view/<int:role_id>')
@login_required
def role_view(role_id):
    role = find_role_by_id(role_id)
    if role is not None and role.user_may_view(current_user):
        return render_template('role_view.j2', role=role, tab="role")
    else:
        return redirect(url_for('home_bp.home'))


