#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.root_delete_handler import RootDeleteHandler
from tracking.page_handlers.root_update_handler import RootUpdateHandler
from tracking.page_handlers.root_view_handler import RootViewHandler

root_bp = Blueprint(
    'root_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@root_bp.route('/delete/<activity>/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_delete(**kwargs):
    return RootDeleteHandler(current_user, **kwargs).handle()


@root_bp.route('/update/<activity>/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['GET', 'POST'])
@login_required
def root_update(**kwargs):
    return RootUpdateHandler(current_user, **kwargs).handle()


@root_bp.route('/view/<activity>/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_view(**kwargs):
    return RootViewHandler(current_user, **kwargs).handle()
