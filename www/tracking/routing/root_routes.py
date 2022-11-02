#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import login_required, current_user

from tracking.page_handlers.root_delete_handler import RootDeleteHandler
from tracking.page_handlers.root_update_handler import RootUpdateHandler
from tracking.page_handlers.root_view_handler import RootViewHandler
from tracking.routing.home_redirect import home_redirect

root_bp = Blueprint(
    'root_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@root_bp.route('/delete/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_delete(place_id, thing_id, specification_id):
    handler = RootDeleteHandler(current_user, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()


@root_bp.route('/update/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['GET', 'POST'])
@login_required
def root_update(place_id, thing_id, specification_id):
    handler = RootUpdateHandler(current_user, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()


@root_bp.route('/view/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_view(place_id, thing_id, specification_id):
    handler = RootViewHandler(current_user, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()
