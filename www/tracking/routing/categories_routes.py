#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.categories_create_handler import CategoriesCreateHandler
from tracking.page_handlers.categories_view_handler import CategoriesViewHandler

categories_bp = Blueprint(
    'categories_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@categories_bp.route('/create/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def categories_create(**kwargs):
    return CategoriesCreateHandler(current_user, **kwargs).handle()


@categories_bp.route('/view/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>')
@login_required
def categories_view(**kwargs):
    return CategoriesViewHandler(current_user, **kwargs).handle()
