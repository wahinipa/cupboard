#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.refinement_add_handler import RefinementAddHandler
from tracking.page_handlers.refinement_remove_handler import RefinementRemoveHandler

refinement_bp = Blueprint(
    'refinement_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@refinement_bp.route('/add/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                     methods=['POST', 'GET'])
@login_required
def refinement_add(**kwargs):
    return RefinementAddHandler(current_user, **kwargs).handle()


@refinement_bp.route('/remove/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                     methods=['POST', 'GET'])
@login_required
def refinement_remove(category_id, **kwargs):
    return RefinementRemoveHandler(current_user, category_id, **kwargs).handle()
