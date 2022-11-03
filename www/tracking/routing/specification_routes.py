#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.specification_update_handler import SpecificationUpdateHandler

specification_bp = Blueprint(
    'specification_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@specification_bp.route('/update/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                        methods=['GET', 'POST'])
@login_required
def specification_update(**kwargs):
    return SpecificationUpdateHandler(current_user, **kwargs).handle()
