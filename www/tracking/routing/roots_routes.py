#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import login_required, current_user

from tracking.page_handlers.roots_create_handler import RootsCreateHandler
from tracking.page_handlers.roots_view_handler import RootsViewHandler
from tracking.routing.home_redirect import home_redirect

roots_bp = Blueprint(
    'roots_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@roots_bp.route('/create', methods=['POST', 'GET'])
@login_required
def roots_create():
    handler = RootsCreateHandler(current_user)
    return handler.render() or home_redirect()


@roots_bp.route('/view')
@login_required
def roots_view():
    handler = RootsViewHandler(current_user)
    return handler.render() or home_redirect()
