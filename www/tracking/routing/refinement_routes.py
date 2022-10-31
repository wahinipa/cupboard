#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint, redirect
from flask_login import login_required, current_user

from tracking.modelling.category_model import find_category_by_id
from tracking.viewers.placement_model import create_placement
from tracking.modelling.refinement_model import add_refinement, remove_refinement
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
    category = find_category_by_id(category_id)
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if category and placement.may_be_observed(current_user) and placement.root == category.root \
        and category.may_update(current_user):
        thing = placement.thing
        navigator = placement.create_navigator()
        redirect_url = navigator.url(category, 'view')
        add_refinement(thing, category)
        return redirect(redirect_url)
    else:
        return home_redirect()


@refinement_bp.route('/remove/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                     methods=['POST', 'GET'])
@login_required
def refinement_remove(category_id, place_id, thing_id, specification_id):
    category = find_category_by_id(category_id)
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if category and placement.may_be_observed(current_user) and placement.root == category.root and category.may_update(
        current_user):
        thing = placement.thing
        navigator = placement.create_navigator()
        redirect_url = navigator.url(category, 'view')
        remove_refinement(thing, category)
        return redirect(redirect_url)
    else:
        return home_redirect()
