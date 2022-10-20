#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, redirect, request, url_for
from flask_login import current_user, login_required

from tracking import database
from tracking.forms.choice_forms import ChoiceUpdateForm
from tracking.modelling.choice_models import find_choice_by_id
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.thing_model import find_thing_by_id
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect

choice_bp = Blueprint(
    'choice_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@choice_bp.route('/delete/<int:choice_id>/<int:place_id>/<int:thing_id>')
@login_required
def choice_delete(choice_id, place_id, thing_id):
    choice = find_choice_by_id(choice_id)
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if choice and place and thing and choice.may_delete(current_user):
        navigator = DualNavigator(root=choice.root, place=place, thing=thing)
        redirect_url = navigator.url(choice.category, 'view')
        database.session.delete(choice)
        database.session.commit()
        return redirect(redirect_url)
    else:
        return home_redirect()


@choice_bp.route('/view/<int:choice_id>/<int:place_id>/<int:thing_id>')
@login_required
def choice_view(choice_id, place_id, thing_id):
    choice = find_choice_by_id(choice_id)
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if choice and place and thing and choice.may_be_observed(current_user):
        navigator = DualNavigator(root=choice.root, place=place, thing=thing)
        display_attributes = {
            'description': True,
            'url': True,
            'bread_crumbs': True,
        }
        return choice.display_context(navigator, current_user, display_attributes).render_template("pages/choice_view.j2")
    else:
        return home_redirect()


@choice_bp.route('/update/<int:choice_id>/<int:place_id>/<int:thing_id>', methods=['GET', 'POST'])
@login_required
def choice_update(choice_id, place_id, thing_id):
    choice = find_choice_by_id(choice_id)
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if choice and place and thing and choice.may_update(current_user):
        navigator = DualNavigator(root=choice.root, place=place, thing=thing)
        form = choice_update_form(choice)
        redirect_url = navigator.url(choice, 'view')
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(redirect_url)
        if form.validate_on_submit():
            update_choice_from_form(choice, form)
            database.session.commit()
            return redirect(redirect_url)
        else:
            return choice.display_context(navigator, current_user).render_template(
                'pages/form_page.j2', form=form, form_title=f'Update {choice.name}')
    else:
        return home_redirect()


def choice_update_form(choice):
    return ChoiceUpdateForm(obj=choice)


def update_choice_from_form(choice, form):
    form.populate_obj(choice)
