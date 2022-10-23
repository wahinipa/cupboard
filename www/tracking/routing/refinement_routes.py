#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint, url_for, request, redirect
from flask_login import login_required, current_user

from tracking.modelling.category_model import find_category_by_id
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.refinement_model import add_refinement, remove_refinement
from tracking.modelling.thing_model import find_thing_by_id
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect

refinement_bp = Blueprint(
    'refinement_bp', __name__,
    template_folder='templates',
    static_folder='static',
)

@refinement_bp.route('/add/<int:category_id>/<int:place_id>/<int:thing_id>', methods=['POST', 'GET'])
@login_required
def refinement_add(category_id, place_id, thing_id):
    category = find_category_by_id(category_id)
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if category and place and thing and place.root == category.root \
        and thing.root == category.root and category.may_update(current_user):
        navigator = DualNavigator(place=place, thing=thing)
        redirect_url = navigator.url(category, 'view')
        add_refinement(thing, category)
        return redirect(redirect_url)
    else:
        return home_redirect()

@refinement_bp.route('/remove/<int:category_id>/<int:place_id>/<int:thing_id>', methods=['POST', 'GET'])
@login_required
def refinement_remove(category_id, place_id, thing_id):
    category = find_category_by_id(category_id)
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if category and place and thing and place.root == category.root \
        and thing.root == category.root and category.may_update(current_user):
        navigator = DualNavigator(place=place, thing=thing)
        redirect_url = navigator.url(category, 'view')
        remove_refinement(thing, category)
        return redirect(redirect_url)
    else:
        return home_redirect()
