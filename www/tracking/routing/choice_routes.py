#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.choice_delete_handler import ChoiceDeleteHandler
from tracking.page_handlers.choice_update_handler import ChoiceUpdateHandler
from tracking.page_handlers.choice_view_handler import ChoiceViewHandler

choice_bp = Blueprint(
    'choice_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@choice_bp.route('/delete/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>/<int:choice_id>')
@login_required
def choice_delete(**kwargs):
    return ChoiceDeleteHandler('choice_bp.choice_delete', current_user, **kwargs).handle()


@choice_bp.route('/view/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>/<int:choice_id>')
@login_required
def choice_view(**kwargs):
    return ChoiceViewHandler('choice_bp.choice_view', current_user, **kwargs).handle()


@choice_bp.route('/update/<activity>/<int:place_id>/<int:destination_id>/<int:thing_id>/<int:specification_id>/<int:choice_id>',
                 methods=['GET', 'POST'])
@login_required
def choice_update(**kwargs):
    return ChoiceUpdateHandler('choice_bp.choice_update', current_user, **kwargs).handle()
