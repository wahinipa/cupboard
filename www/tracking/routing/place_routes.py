#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint
from flask_login import login_required, current_user

from tracking.page_handlers.place_create_handler import PlaceCreateHandler
from tracking.page_handlers.place_delete_handler import PlaceDeleteHandler
from tracking.page_handlers.place_update_handler import PlaceUpdateHandler
from tracking.routing.home_redirect import home_redirect

place_bp = Blueprint(
    'place_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@place_bp.route('/create/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def place_create(place_id, thing_id, specification_id):
    handler = PlaceCreateHandler(current_user, place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    return handler.render() or home_redirect()


@place_bp.route('/delete/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def place_delete(place_id, thing_id, specification_id):
    handler = PlaceDeleteHandler(current_user, place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    return handler.render() or home_redirect()


@place_bp.route('/update/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['GET', 'POST'])
@login_required
def place_update(place_id, thing_id, specification_id):
    handler = PlaceUpdateHandler(current_user, place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    return handler.render() or home_redirect()
