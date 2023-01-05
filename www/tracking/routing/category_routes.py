#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.category_choice_create_handler import CategoryChoiceCreateHandler
from tracking.page_handlers.category_delete_handler import CategoryDeleteHandler
from tracking.page_handlers.category_update_handler import CategoryUpdateHandler
from tracking.page_handlers.category_view_handler import CategoryViewHandler
from tracking.page_handlers.refinement_add_handler import RefinementAddHandler
from tracking.page_handlers.refinement_remove_handler import RefinementRemoveHandler

category_bp = Blueprint(
    'category_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@category_bp.route(
    '/delete/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>/<int:category_id>')
@login_required
def category_delete(**kwargs):
    return CategoryDeleteHandler('category_bp.category_delete'.current_user, **kwargs).handle()


@category_bp.route(
    '/view/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>/<int:category_id>')
@login_required
def category_view(**kwargs):
    return CategoryViewHandler('category_bp.category_view', current_user, **kwargs).handle()


@category_bp.route(
    '/update/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>/<int:category_id>',
    methods=['GET', 'POST'])
@login_required
def category_update(**kwargs):
    return CategoryUpdateHandler('category_bp.category_update', current_user, **kwargs).handle()


@category_bp.route(
    '/create/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>/<int:category_id>',
    methods=['POST', 'GET'])
@login_required
def category_create(**kwargs):
    return CategoryChoiceCreateHandler('category_bp.category_create', current_user, **kwargs).handle()


@category_bp.route(
    '/add/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>/<int:category_id>',
    methods=['POST', 'GET'])
@login_required
def category_add(**kwargs):
    return RefinementAddHandler('category_bp.category_add', current_user, **kwargs).handle()


@category_bp.route(
    '/remove/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>/<int:category_id>',
    methods=['POST', 'GET'])
@login_required
def category_remove(category_id, **kwargs):
    return RefinementRemoveHandler('category_bp.category_remove', current_user, category_id, **kwargs).handle()
