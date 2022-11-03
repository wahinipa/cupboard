#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.roots_create_handler import RootsCreateHandler
from tracking.page_handlers.roots_view_handler import RootsViewHandler

roots_bp = Blueprint(
    'roots_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@roots_bp.route('/create', methods=['POST', 'GET'])
@login_required
def roots_create():
    return RootsCreateHandler(current_user).handle()


@roots_bp.route('/view')
@login_required
def roots_view():
    return RootsViewHandler(current_user).handle()
