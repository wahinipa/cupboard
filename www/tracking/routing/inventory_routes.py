#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.inventory_adjustment_handler import InventoryAdjustmentHandler
from tracking.page_handlers.inventory_arrival_handler import InventoryArrivalHandler
from tracking.page_handlers.inventory_departure_handler import InventoryDepartureHandler
from tracking.page_handlers.inventory_transfer_handler import InventoryTransferHandler

inventory_bp = Blueprint(
    'inventory_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@inventory_bp.route('/arriving/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>',
                    methods=['POST', 'GET'])
@login_required
def inventory_arriving(**kwargs):
    return InventoryArrivalHandler(current_user, **kwargs).handle()


@inventory_bp.route('/departing/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>',
                    methods=['POST', 'GET'])
@login_required
def inventory_departing(**kwargs):
    return InventoryDepartureHandler(current_user, **kwargs).handle()


@inventory_bp.route('/moving/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>',
                    methods=['POST', 'GET'])
@login_required
def inventory_moving(**kwargs):
    return InventoryTransferHandler(current_user, **kwargs).handle()


@inventory_bp.route('/changing/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>',
                    methods=['POST', 'GET'])
@login_required
def inventory_changing(**kwargs):
    return InventoryAdjustmentHandler(current_user, **kwargs).handle()
