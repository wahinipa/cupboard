#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.specification_update_handler import SpecificationUpdateHandler

specification_bp = Blueprint(
    'specification_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@specification_bp.route('/update/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>/<int:category_id>',
                        methods=['GET', 'POST'])
@login_required
def specification_update(**kwargs):
    return SpecificationUpdateHandler(current_user, **kwargs).handle()
