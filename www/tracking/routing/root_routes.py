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
    return RootDeleteHandler(current_user, **kwargs).handle()


@root_bp.route('/update/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>',
               methods=['GET', 'POST'])
@login_required
def root_update(**kwargs):
    return RootUpdateHandler(current_user, **kwargs).handle()


@root_bp.route('/view/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_view(activity, **kwargs):
    handler = root_view_handler_selection.get(activity, RootObserveHandler)
    return handler('root_bp.root_view', current_user, activity=activity, **kwargs).handle()

root_view_handler_selection = {
    'observe': RootObserveHandler,
    'inbound': RootInboundHandler,
    'outbound': RootOutboundHandler,
    'transfer': RootTransferHandler,
    'adjust': RootAdjustHandler,
}
