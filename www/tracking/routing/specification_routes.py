#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint
from flask_login import login_required, current_user

from tracking.page_handlers.specification_update_handler import SpecificationUpdateHandler
from tracking.routing.home_redirect import home_redirect

specification_bp = Blueprint(
    'specification_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@specification_bp.route('/update/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                        methods=['GET', 'POST'])
@login_required
def specification_update(category_id, place_id, thing_id, specification_id):
    handler = SpecificationUpdateHandler(current_user, category_id, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()
