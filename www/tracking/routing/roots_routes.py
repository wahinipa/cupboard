#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.people_view_handler import PeopleViewHandler
from tracking.page_handlers.root_observe_handler import RootObserveHandler
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
    return RootsCreateHandler('roots_bp.roots_create', current_user).handle()


@roots_bp.route('/view')
@login_required
def roots_view():
    root = current_user.only_root
    if root:
        handler = RootObserveHandler('roots_bp.roots_view', current_user, root_id=root.id)
    elif current_user.is_rootless:
        handler = PeopleViewHandler('people_bp.people_view', current_user, person_id=current_user.id)
    else:
        handler = RootsViewHandler('roots_bp.roots_view', current_user)
    return handler.handle()
