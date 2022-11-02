#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint
from flask_login import login_required, current_user

from tracking.page_handlers.thing_create_handler import ThingCreateHandler
from tracking.page_handlers.thing_delete_handler import ThingDeleteHandler
from tracking.page_handlers.thing_update_handler import ThingUpdateHandler
from tracking.routing.home_redirect import home_redirect

thing_bp = Blueprint(
    'thing_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@thing_bp.route('/create/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def thing_create(place_id, thing_id, specification_id):
    handler = ThingCreateHandler(current_user, place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    return handler.render() or home_redirect()


@thing_bp.route('/delete/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def thing_delete(place_id, thing_id, specification_id):
    handler = ThingDeleteHandler(current_user, place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    return handler.render() or home_redirect()


@thing_bp.route('/update/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['GET', 'POST'])
@login_required
def thing_update(place_id, thing_id, specification_id):
    handler = ThingUpdateHandler(current_user, place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    return handler.render() or home_redirect()
