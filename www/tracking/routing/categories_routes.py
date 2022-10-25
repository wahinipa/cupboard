#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking.forms.category_forms import CategoryCreateForm
from tracking.modelling.categories_model import Categories
from tracking.modelling.particular_thing_model import find_particular_thing_by_id
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.placement_model import create_placement
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect
from tracking.viewing.card_display_attributes import dual_view_childrens_attributes
from tracking.viewing.cupboard_display_context import CupboardDisplayContext

categories_bp = Blueprint(
    'categories_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@categories_bp.route('/create/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def categories_create(place_id, thing_id, specification_id):
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if placement.may_be_observed(current_user) and placement.root.may_create_category(
        current_user):
        place = placement.place
        thing = placement.thing
        specification = placement.specification
        form = CategoryCreateForm()
        navigator = placement.create_navigator()
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(navigator.url(Categories(place, thing, specification), 'view'))
        if form.validate_on_submit():
            category = place.root.create_category(form.name.data, form.description.data)
            return redirect(navigator.url(category, 'view'))
        else:
            return CupboardDisplayContext().render_template('pages/form_page.j2', form=form,
                                                            form_title=f'Create New Category for {place.root.name}')
    else:
        return home_redirect()


@categories_bp.route('/view/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def categories_view(place_id, thing_id, specification_id):
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if placement.may_be_observed(current_user) and placement.root.may_be_observed(current_user):
        place = placement.place
        thing = placement.thing
        specification = placement.specification
        navigator = placement.create_navigator()
        categories = Categories(place=place, thing=thing, specification=specification)
        display_attributes = {
            'description': True,
            'children': [categories, placement.particular_thing],
            'children_attributes': dual_view_childrens_attributes(),
        }
        place_url = navigator.url(place.root, 'view')
        category_list_url = navigator.url(categories, 'view')
        return place.root.display_context(navigator, current_user, display_attributes).render_template(
            "pages/category_list.j2", place_url=place_url, category_list_url=category_list_url,
            active_flavor='category')
    return home_redirect()
