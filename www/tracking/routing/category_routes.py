#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.category_choice_create_handler import CategoryChoiceCreateHandler
from tracking.page_handlers.category_delete_handler import CategoryDeleteHandler
from tracking.page_handlers.category_update_handler import CategoryUpdateHandler
from tracking.page_handlers.category_view_handler import CategoryViewHandler
from tracking.routing.home_redirect import home_redirect

category_bp = Blueprint(
    'category_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@category_bp.route('/delete/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def category_delete(category_id, place_id, thing_id, specification_id):
    handler = CategoryDeleteHandler(current_user, category_id, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()


@category_bp.route('/view/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def category_view(category_id, place_id, thing_id, specification_id):
    handler = CategoryViewHandler(current_user, category_id, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()


@category_bp.route('/update/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                   methods=['GET', 'POST'])
@login_required
def category_update(category_id, place_id, thing_id, specification_id):
    handler = CategoryUpdateHandler(current_user, category_id, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()


@category_bp.route('/create/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                   methods=['POST', 'GET'])
@login_required
def category_create(category_id, place_id, thing_id, specification_id):
    handler = CategoryChoiceCreateHandler(current_user, category_id, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()
