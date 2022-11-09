#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.place_create_handler import PlaceCreateHandler
from tracking.page_handlers.place_delete_handler import PlaceDeleteHandler
from tracking.page_handlers.place_update_handler import PlaceUpdateHandler

place_bp = Blueprint(
    'place_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@place_bp.route('/create/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def place_create(**kwargs):
    return PlaceCreateHandler(current_user, **kwargs).handle()


@place_bp.route('/delete/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>')
@login_required
def place_delete(**kwargs):
    return PlaceDeleteHandler(current_user, **kwargs).handle()


@place_bp.route('/update/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>', methods=['GET', 'POST'])
@login_required
def place_update(**kwargs):
    return PlaceUpdateHandler(current_user, **kwargs).handle()
