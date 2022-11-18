#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import current_user, login_required

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
