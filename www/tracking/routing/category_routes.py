#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, redirect, request
from flask_login import current_user, login_required

from tracking import database
from tracking.forms.category_forms import CategoryUpdateForm, update_category_from_form
from tracking.forms.choice_forms import ChoiceCreateForm
from tracking.modelling.categories_model import Categories
from tracking.modelling.category_model import find_category_by_id
from tracking.modelling.placement_model import create_placement
from tracking.routing.home_redirect import home_redirect
from tracking.viewing.card_display_attributes import dual_view_childrens_attributes
from tracking.viewing.cupboard_display_context import CupboardDisplayContext

category_bp = Blueprint(
    'category_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@category_bp.route('/delete/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def category_delete(category_id, place_id, thing_id, specification_id):
    category = find_category_by_id(category_id)
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if category and placement.may_be_observed(current_user) and placement.root == category.root and category.may_delete(
        current_user):
        navigator = placement.create_navigator()
        place = placement.place
        thing = placement.thing
        specification = placement.specification
        categories = Categories(place=place, thing=thing, specification=specification)
        redirect_url = navigator.url(categories, 'view')
        database.session.delete(category)
        database.session.commit()
        return redirect(redirect_url)
    else:
        return home_redirect()


@category_bp.route('/view/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def category_view(category_id, place_id, thing_id, specification_id):
    category = find_category_by_id(category_id)
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if category and placement.may_be_observed(
        current_user) and placement.root == category.root and category.may_be_observed(
        current_user):
        navigator = placement.create_navigator()
        place = placement.place
        thing = placement.thing
        specification = placement.specification
        display_attributes = {
            'description': True,
            'children': [category, placement.particular_thing],
            'children_attributes': dual_view_childrens_attributes(thing=thing),
        }
        place_url = navigator.url(place.root, 'view')
        category_list_url = navigator.url(Categories(place=place, thing=thing, specification=specification), 'view')
        return place.root.display_context(navigator, current_user, display_attributes).render_template(
            "pages/category_view.j2", category_list_url=category_list_url, place_url=place_url,
            active_flavor='category')
    else:
        return home_redirect()


@category_bp.route('/update/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                   methods=['GET', 'POST'])
@login_required
def category_update(category_id, place_id, thing_id, specification_id):
    category = find_category_by_id(category_id)
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if category and placement.may_be_observed(current_user) and placement.root == category.root and category.may_update(
        current_user):
        navigator = placement.create_navigator()
        form = CategoryUpdateForm(obj=category)
        redirect_url = navigator.url(category, 'view')
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(redirect_url)
        if form.validate_on_submit():
            update_category_from_form(category, form)
            database.session.commit()
            return redirect(redirect_url)
        else:
            return CupboardDisplayContext().render_template(
                'pages/form_page.j2', form=form, form_title=f'Update {category.name}')
    else:
        return home_redirect()


@category_bp.route('/create/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                   methods=['POST', 'GET'])
@login_required
def category_create(category_id, place_id, thing_id, specification_id):
    category = find_category_by_id(category_id)
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if placement.may_be_observed(current_user) and placement.root == category.root and category.may_create_choice(
        current_user):
        form = ChoiceCreateForm()
        navigator = placement.create_navigator()
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(navigator.url(category, 'view'))
        if form.validate_on_submit():
            choice = category.create_choice(form.name.data, form.description.data)
            return redirect(navigator.url(choice, 'view'))
        else:
            return CupboardDisplayContext().render_template('pages/form_page.j2', form=form,
                                                            form_title=f'Create New Choice for {category.name}')
    else:
        return home_redirect()
