#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking.viewing.cupboard_display_context import CupboardDisplayContext
from tracking.forms.category_forms import CategoryCreateForm
from tracking.modelling.category_models import Categories
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.root_model import find_root_by_id
from tracking.modelling.thing_model import find_thing_by_id
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect

categories_bp = Blueprint(
    'categories_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@categories_bp.route('/create/<int:root_id>/<int:place_id>/<int:thing_id>', methods=['POST', 'GET'])
@login_required
def categories_create(root_id, place_id, thing_id):
    root = find_root_by_id(root_id)
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if root and place and thing and root.may_create_category(current_user):
        form = CategoryCreateForm()
        navigator = DualNavigator(root=root, place=place, thing=thing)
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(navigator.url(Categories(root, place, thing), 'view'))
        if form.validate_on_submit():
            category = root.create_category(form.name.data, form.description.data)
            return redirect(navigator.url(category, 'view'))
        else:
            return CupboardDisplayContext().render_template('pages/form_page.j2', form=form,
                                                            form_title=f'Create New Category for {root.name}')
    else:
        return home_redirect()


@categories_bp.route('/view/<int:root_id>/<int:place_id>/<int:thing_id>')
@login_required
def categories_view(root_id, place_id, thing_id):
    root = find_root_by_id(root_id)
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if root and place and thing and root.may_be_observed(current_user):
        navigator = DualNavigator(root=root, place=place, thing=thing)
        categories = Categories(root=root, place=place, thing=thing)
        return categories.display_context(navigator, current_user, child_depth=1).render_template(
            "pages/category_list.j2")
    return home_redirect()
