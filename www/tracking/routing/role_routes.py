#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.role_list_handler import RoleListHandler
from tracking.page_handlers.role_view_handler import RoleViewHandler

role_bp = Blueprint(
    'role_bp', __name__,
    template_folder='templates',
    static_folder='static',
)

@role_bp.route('/list')
@login_required
def role_list():
    return RoleListHandler('role_bp.role_list', current_user).handle()


@role_bp.route('/view/<int:role_id>')
@login_required
def role_view(role_id):
    return RoleViewHandler('role_bp.role_view', current_user, role_id=role_id).handle()
