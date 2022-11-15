#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.root_adjust_handler import RootAdjustHandler
from tracking.page_handlers.root_inbound_handler import RootInboundHandler
from tracking.page_handlers.root_observe_handler import RootObserveHandler
from tracking.page_handlers.root_delete_handler import RootDeleteHandler
from tracking.page_handlers.root_outbound_handler import RootOutboundHandler
from tracking.page_handlers.root_transfer_handler import RootTransferHandler
from tracking.page_handlers.root_update_handler import RootUpdateHandler

root_bp = Blueprint(
    'root_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@root_bp.route('/delete/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_delete(**kwargs):
    return RootDeleteHandler('root_bp.root_delete', current_user, **kwargs).handle()


@root_bp.route('/update/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>',
               methods=['GET', 'POST'])
@login_required
def root_update(**kwargs):
    return RootUpdateHandler('root_bp.root_update', current_user, **kwargs).handle()


@root_bp.route('/view/observe/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_view_observe(**kwargs):
    return RootObserveHandler('root_bp.root_view_observe', current_user, activity='observe', **kwargs).handle()

@root_bp.route('/view/inbound/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_view_inbound(**kwargs):
    return RootInboundHandler('root_bp.root_view_inbound', current_user, activity='inbound', **kwargs).handle()

@root_bp.route('/view/outbound/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_view_outbound(**kwargs):
    return RootOutboundHandler('root_bp.root_view_outbound', current_user, activity='outbound', **kwargs).handle()

@root_bp.route('/view/transfer/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_view_transfer(**kwargs):
    return RootTransferHandler('root_bp.root_view_transfer', current_user, activity='transfer', **kwargs).handle()

@root_bp.route('/view/adjust/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_view_adjust(**kwargs):
    return RootAdjustHandler('root_bp.root_view_adjust', current_user, activity='adjust', **kwargs).handle()

