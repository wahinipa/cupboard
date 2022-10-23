#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint, redirect
from flask_login import login_required, current_user

from tracking.modelling.category_model import find_category_by_id
from tracking.modelling.particular_thing_model import find_particular_thing_by_id
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.refinement_model import add_refinement, remove_refinement
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect

refinement_bp = Blueprint(
    'refinement_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@refinement_bp.route('/add/<int:category_id>/<int:place_id>/<int:particular_thing_id>', methods=['POST', 'GET'])
@login_required
def refinement_add(category_id, place_id, particular_thing_id):
    category = find_category_by_id(category_id)
    place = find_place_by_id(place_id)
    particular_thing = find_particular_thing_by_id(particular_thing_id)
    if category and place and particular_thing and place.root == category.root \
        and particular_thing.root == category.root and category.may_update(current_user):
        navigator = DualNavigator(place=place, particular_thing=particular_thing)
        redirect_url = navigator.url(category, 'view')
        add_refinement(particular_thing, category)
        return redirect(redirect_url)
    else:
        return home_redirect()


@refinement_bp.route('/remove/<int:category_id>/<int:place_id>/<int:particular_thing_id>', methods=['POST', 'GET'])
@login_required
def refinement_remove(category_id, place_id, particular_thing_id):
    category = find_category_by_id(category_id)
    place = find_place_by_id(place_id)
    particular_thing = find_particular_thing_by_id(particular_thing_id)
    if category and place and particular_thing and place.root == category.root \
        and particular_thing.root == category.root and category.may_update(current_user):
        navigator = DualNavigator(place=place, particular_thing=particular_thing)
        redirect_url = navigator.url(category, 'view')
        remove_refinement(particular_thing, category)
        return redirect(redirect_url)
    else:
        return home_redirect()
