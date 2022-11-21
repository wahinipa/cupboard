#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.role_deny_handler import RoleDenyHandler
from tracking.page_handlers.role_grant_handler import RoleGrantHandler
from tracking.page_handlers.role_view_handler import RoleViewHandler

role_bp = Blueprint(
    'role_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@role_bp.route('/view/<int:role_id>/<int:place_id>/<int:person_id>')
@login_required
def role_view(role_id, place_id, person_id):
    return RoleViewHandler('role_bp.role_view', current_user, role_id=role_id, place_id=place_id,
                           person_id=person_id).handle()


@role_bp.route('/grant/<int:role_id>/<int:place_id>/<int:person_id>')
@login_required
def role_grant(role_id, place_id, person_id):
    return RoleGrantHandler('role_bp.role_grant', current_user, role_id=role_id, place_id=place_id,
                           person_id=person_id).handle()


@role_bp.route('/deny/<int:role_id>/<int:place_id>/<int:person_id>')
@login_required
def role_deny(role_id, place_id, person_id):
    return RoleDenyHandler('role_bp.role_deny', current_user, role_id=role_id, place_id=place_id,
                           person_id=person_id).handle()
