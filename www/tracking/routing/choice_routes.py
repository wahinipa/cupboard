#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, redirect, request
from flask_login import current_user, login_required

from tracking import database
from tracking.forms.choice_forms import ChoiceUpdateForm, update_choice_from_form
from tracking.viewers.categories_model import Categories
from tracking.modelling.choice_model import find_choice_by_id
from tracking.viewers.platter import create_platter
from tracking.routing.home_redirect import home_redirect
from tracking.contexts.card_display_attributes import dual_view_childrens_attributes
from tracking.contexts.cupboard_display_context import CupboardDisplayContext

choice_bp = Blueprint(
    'choice_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@choice_bp.route('/delete/<int:choice_id>/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def choice_delete(choice_id, place_id, thing_id, specification_id):
    choice = find_choice_by_id(choice_id)
    platter = create_platter(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if choice and platter.may_be_observed(current_user) and platter.root == choice.root and choice.may_delete(
        current_user):
        navigator = platter.create_navigator()
        redirect_url = navigator.url(choice.category, 'view')
        database.session.delete(choice)
        database.session.commit()
        return redirect(redirect_url)
    else:
        return home_redirect()


@choice_bp.route('/view/<int:choice_id>/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def choice_view(choice_id, place_id, thing_id, specification_id):
    choice = find_choice_by_id(choice_id)
    platter = create_platter(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if choice and platter.may_be_observed(current_user) and platter.root == choice.root and choice.may_be_observed(
        current_user):
        navigator = platter.create_navigator()
        place = platter.place
        thing = platter.thing
        specification = platter.specification
        display_attributes = {
            'description': True,
            'children': [choice, platter.thing, platter.thing_specification],
            'children_attributes': dual_view_childrens_attributes(),
        }
        place_url = navigator.url(platter.root, 'view')
        category_list_url = navigator.url(Categories(place=place, thing=thing, specification=specification), 'view')
        return platter.thing_specification.display_context(navigator, current_user, display_attributes).render_template(
            "pages/choice_view.j2", category_list_url=category_list_url, place_url=place_url,
            active_flavor='category')
    else:
        return home_redirect()


@choice_bp.route('/update/<int:choice_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                 methods=['GET', 'POST'])
@login_required
def choice_update(choice_id, place_id, thing_id, specification_id):
    choice = find_choice_by_id(choice_id)
    platter = create_platter(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if choice and platter.may_be_observed(current_user) and platter.root == choice.root and choice.may_update(
        current_user):
        navigator = platter.create_navigator()
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
