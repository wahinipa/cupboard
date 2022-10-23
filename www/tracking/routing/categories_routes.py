#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking.forms.category_forms import CategoryCreateForm
from tracking.modelling.categories_model import Categories
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.thing_model import find_thing_by_id
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect
from tracking.viewing.card_display_attributes import dual_view_childrens_attributes
from tracking.viewing.cupboard_display_context import CupboardDisplayContext

categories_bp = Blueprint(
    'categories_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@categories_bp.route('/create/<int:place_id>/<int:thing_id>', methods=['POST', 'GET'])
@login_required
def categories_create(place_id, thing_id):
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if place and thing and place.root == thing.root and place.root.may_create_category(current_user):
        form = CategoryCreateForm()
        navigator = DualNavigator(place=place, thing=thing)
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(navigator.url(Categories(place, thing), 'view'))
        if form.validate_on_submit():
            category = place.root.create_category(form.name.data, form.description.data)
            return redirect(navigator.url(category, 'view'))
        else:
            return CupboardDisplayContext().render_template('pages/form_page.j2', form=form,
                                                            form_title=f'Create New Category for {place.root.name}')
    else:
        return home_redirect()


@categories_bp.route('/view/<int:place_id>/<int:thing_id>')
@login_required
def categories_view(place_id, thing_id):
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if place and thing and place.root == thing.root and place.root.may_be_observed(current_user):
        navigator = DualNavigator(place=place, thing=thing)
        categories = Categories(place=place, thing=thing)
        display_attributes = {
            'description': True,
            'children': [categories, thing],
            'children_attributes': dual_view_childrens_attributes(),
        }
        place_url = navigator.url(place.root, 'view')
        category_list_url = navigator.url(Categories(place=place, thing=thing), 'view')
        return place.root.display_context(navigator, current_user, display_attributes).render_template(
            "pages/category_list.j2", place_url=place_url, category_list_url=category_list_url,
            active_flavor='category')
    return home_redirect()
