#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint
from flask_login import current_user, login_required

from tracking.page_handlers.choice_delete_handler import ChoiceDeleteHandler
from tracking.page_handlers.choice_update_handler import ChoiceUpdateHandler
from tracking.page_handlers.choice_view_handler import ChoiceViewHandler
from tracking.routing.home_redirect import home_redirect

choice_bp = Blueprint(
    'choice_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@choice_bp.route('/delete/<int:choice_id>/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def choice_delete(choice_id, place_id, thing_id, specification_id):
    handler = ChoiceDeleteHandler(current_user, choice_id, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()


@choice_bp.route('/view/<int:choice_id>/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def choice_view(choice_id, place_id, thing_id, specification_id):
    handler = ChoiceViewHandler(current_user, choice_id, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()


@choice_bp.route('/update/<int:choice_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                 methods=['GET', 'POST'])
@login_required
def choice_update(choice_id, place_id, thing_id, specification_id):
    handler = ChoiceUpdateHandler(current_user, choice_id, place_id, thing_id, specification_id)
    return handler.render() or home_redirect()
