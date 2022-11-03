#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.inventory_arrival_handler import InventoryArrivalHandler
from tracking.page_handlers.inventory_departure_handler import InventoryDepartureHandler
from tracking.routing.home_redirect import home_redirect

inventory_bp = Blueprint(
    'inventory_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@inventory_bp.route('/arriving/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def inventory_arriving(place_id, thing_id, specification_id):
    return InventoryArrivalHandler(current_user, place_id, thing_id, specification_id).handle()


@inventory_bp.route('/departing/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def inventory_departing(thing_id, place_id, specification_id):
    return InventoryDepartureHandler(current_user, place_id, thing_id, specification_id).handle()


@inventory_bp.route('/moving/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def inventory_moving(place_id, thing_id, specification_id):
    return home_redirect()
