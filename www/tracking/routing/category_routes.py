#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, redirect, request
from flask_login import current_user, login_required

from tracking import database
from tracking.forms.category_forms import CategoryUpdateForm, update_category_from_form
from tracking.forms.choice_forms import ChoiceCreateForm
from tracking.modelling.categories_model import Categories
from tracking.modelling.category_model import find_category_by_id
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.thing_model import find_thing_by_id
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect
from tracking.viewing.card_display_attributes import dual_view_childrens_attributes
from tracking.viewing.cupboard_display_context import CupboardDisplayContext

category_bp = Blueprint(
    'category_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@category_bp.route('/delete/<int:category_id>/<int:place_id>/<int:thing_id>')
@login_required
def category_delete(category_id, place_id, thing_id):
    category = find_category_by_id(category_id)
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if category and place and thing and place.root == category.root \
        and thing.root == category.root and category.may_delete(current_user):
        navigator = DualNavigator(place=place, thing=thing)
        categories = Categories(place=place, thing=thing)
        redirect_url = navigator.url(categories, 'view')
        database.session.delete(category)
        database.session.commit()
        return redirect(redirect_url)
    else:
        return home_redirect()


@category_bp.route('/view/<int:category_id>/<int:place_id>/<int:thing_id>')
@login_required
def category_view(category_id, place_id, thing_id):
    category = find_category_by_id(category_id)
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if category and place and thing and place.root == category.root \
        and thing.root == category.root and category.may_be_observed(current_user):
        navigator = DualNavigator(place=place, thing=thing)
        display_attributes = {
            'description': True,
            'children': [category, thing],
            'children_attributes': dual_view_childrens_attributes,
        }
        place_url = navigator.url(place.root, 'view')
        category_list_url = navigator.url(Categories(place=place, thing=thing), 'view')
        return place.root.display_context(navigator, current_user, display_attributes).render_template(
            "pages/category_view.j2", category_list_url=category_list_url, place_url=place_url,
            active_flavor='category')
    else:
        return home_redirect()


@category_bp.route('/update/<int:category_id>/<int:place_id>/<int:thing_id>', methods=['GET', 'POST'])
@login_required
def category_update(category_id, place_id, thing_id):
    category = find_category_by_id(category_id)
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if category and place and thing and place.root == category.root \
        and thing.root == category.root and category.may_update(current_user):
        navigator = DualNavigator(place=place, thing=thing)
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


@category_bp.route('/create/<int:category_id>/<int:place_id>/<int:thing_id>', methods=['POST', 'GET'])
@login_required
def category_create(category_id, place_id, thing_id):
    category = find_category_by_id(category_id)
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if category and place and thing and place.root == category.root \
        and thing.root == category.root and category.may_create_choice(current_user):
        form = ChoiceCreateForm()
        navigator = DualNavigator(place=place, thing=thing)
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
