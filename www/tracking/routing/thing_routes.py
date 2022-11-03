#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.thing_create_handler import ThingCreateHandler
from tracking.page_handlers.thing_delete_handler import ThingDeleteHandler
from tracking.page_handlers.thing_update_handler import ThingUpdateHandler

thing_bp = Blueprint(
    'thing_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@thing_bp.route('/create/<activity>/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def thing_create(**kwargs):
    return ThingCreateHandler(current_user, **kwargs).handle()


@thing_bp.route('/delete/<activity>/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def thing_delete(**kwargs):
    return ThingDeleteHandler(current_user, **kwargs).handle()


@thing_bp.route('/update/<activity>/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['GET', 'POST'])
@login_required
def thing_update(**kwargs):
    return ThingUpdateHandler(current_user, **kwargs).handle()
