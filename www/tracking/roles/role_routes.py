#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, url_for, redirect, render_template
from flask_login import login_required, current_user

from tracking.commons.display_context import display_context
from tracking.roles.role_models import find_role_by_id

role_bp = Blueprint(
    'role_bp', __name__,
    template_folder='templates',
    static_folder='static',
)

# There is no create, update, delete for Role.
# A new role would require new code to implement it.
# So it should be added to the list in find_or_create_standard_roles.

@role_bp.route('/list')
@login_required
def role_list():
    return render_template('role_list.j2', tab="role")


@role_bp.route('/view/<int:role_id>')
@login_required
def role_view(role_id):
    role = find_role_by_id(role_id)
    if role is not None and role.user_may_view(current_user):
        return render_template('role_view.j2', role=role, tab="role", **display_context())
    else:
        return redirect(url_for('home_bp.home'))
