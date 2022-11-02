#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint
from flask_login import login_required, current_user

from tracking.page_handlers.refinement_add_handler import RefinementAddHandler
from tracking.page_handlers.refinement_remove_handler import RefinementRemoveHandler
from tracking.routing.home_redirect import home_redirect

refinement_bp = Blueprint(
    'refinement_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@refinement_bp.route('/add/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                     methods=['POST', 'GET'])
@login_required
def refinement_add(category_id, place_id, thing_id, specification_id):
    handler = RefinementAddHandler(current_user, category_id, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()


@refinement_bp.route('/remove/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                     methods=['POST', 'GET'])
@login_required
def refinement_remove(category_id, place_id, thing_id, specification_id):
    handler = RefinementRemoveHandler(current_user, category_id, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()
