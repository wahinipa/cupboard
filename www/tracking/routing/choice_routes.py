#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, redirect, request
from flask_login import current_user, login_required

from tracking import database
from tracking.forms.choice_forms import ChoiceUpdateForm, update_choice_from_form
from tracking.modelling.categories_model import Categories
from tracking.modelling.choice_model import find_choice_by_id
from tracking.modelling.particular_thing_model import find_particular_thing_by_id
from tracking.modelling.place_model import find_place_by_id
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect
from tracking.viewing.card_display_attributes import dual_view_childrens_attributes
from tracking.viewing.cupboard_display_context import CupboardDisplayContext

choice_bp = Blueprint(
    'choice_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@choice_bp.route('/delete/<int:choice_id>/<int:place_id>/<int:particular_thing_id>')
@login_required
def choice_delete(choice_id, place_id, particular_thing_id):
    choice = find_choice_by_id(choice_id)
    place = find_place_by_id(place_id)
    particular_thing = find_particular_thing_by_id(particular_thing_id)
    if choice and place and particular_thing and place.root == choice.root \
        and particular_thing.root == choice.root and choice.may_delete(current_user):
        navigator = DualNavigator(place=place, particular_thing=particular_thing)
        redirect_url = navigator.url(choice.category, 'view')
        database.session.delete(choice)
        database.session.commit()
        return redirect(redirect_url)
    else:
        return home_redirect()


@choice_bp.route('/view/<int:choice_id>/<int:place_id>/<int:particular_thing_id>')
@login_required
def choice_view(choice_id, place_id, particular_thing_id):
    choice = find_choice_by_id(choice_id)
    place = find_place_by_id(place_id)
    particular_thing = find_particular_thing_by_id(particular_thing_id)
    if choice and place and particular_thing and place.root == choice.root \
        and particular_thing.root == choice.root and choice.may_be_observed(current_user):
        navigator = DualNavigator(place=place, particular_thing=particular_thing)
        display_attributes = {
            'description': True,
            'children': [choice, particular_thing],
            'children_attributes': dual_view_childrens_attributes(),
        }
        place_url = navigator.url(place.root, 'view')
        category_list_url = navigator.url(Categories(place=place, particular_thing=particular_thing), 'view')
        return place.root.display_context(navigator, current_user, display_attributes).render_template(
            "pages/choice_view.j2", category_list_url=category_list_url, place_url=place_url,
            active_flavor='category')
    else:
        return home_redirect()


@choice_bp.route('/update/<int:choice_id>/<int:place_id>/<int:particular_thing_id>', methods=['GET', 'POST'])
@login_required
def choice_update(choice_id, place_id, particular_thing_id):
    choice = find_choice_by_id(choice_id)
    place = find_place_by_id(place_id)
    particular_thing = find_particular_thing_by_id(particular_thing_id)
    if choice and place and particular_thing and place.root == choice.root \
        and particular_thing.root == choice.root and choice.may_update(current_user):
        navigator = DualNavigator(place=place, particular_thing=particular_thing)
        form = ChoiceUpdateForm(obj=choice)
        redirect_url = navigator.url(choice, 'view')
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(redirect_url)
        if form.validate_on_submit():
            update_choice_from_form(choice, form)
            database.session.commit()
            return redirect(redirect_url)
        else:
            return CupboardDisplayContext().render_template(
                'pages/form_page.j2', form=form, form_title=f'Update {choice.name}')
    else:
        return home_redirect()
