#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import login_required, current_user

from tracking.page_handlers.categories_create_handler import CategoriesCreateHandler
from tracking.page_handlers.categories_view_handler import CategoriesViewHandler
from tracking.routing.home_redirect import home_redirect

categories_bp = Blueprint(
    'categories_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@categories_bp.route('/create/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def categories_create(place_id, thing_id, specification_id):
    handler = CategoriesCreateHandler(current_user, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()


@categories_bp.route('/view/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def categories_view(place_id, thing_id, specification_id):
    handler = CategoriesViewHandler(current_user, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()
