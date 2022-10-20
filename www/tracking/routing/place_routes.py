#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user

from tracking import database
from tracking.forms.place_forms import PlaceCreateForm, PlaceUpdateForm, update_place_from_form
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.thing_model import find_thing_by_id
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect
from tracking.viewing.cupboard_display_context import CupboardDisplayContext

place_bp = Blueprint(
    'place_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@place_bp.route('/create/<int:place_id>/<int:thing_id>', methods=['POST', 'GET'])
@login_required
def place_create(place_id, thing_id):
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if place and thing and place.may_create_place(current_user):
        form = PlaceCreateForm()
        navigator = DualNavigator(place=place, thing=thing)
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(navigator.url(place, 'view'))
        if form.validate_on_submit():
            new_place = place.create_kind_of_place(name=form.name.data, description=form.description.data)
            return redirect(navigator.url(new_place, 'view'))
        else:
            return CupboardDisplayContext().render_template(
                "pages/form_page.j2", form=form, form_title=f'Create New Place for {place.name}')
    else:
        return home_redirect()


@place_bp.route('/delete/<int:place_id>/<int:thing_id>')
@login_required
def place_delete(place_id, thing_id):
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if place and thing and place.may_delete(current_user):
        navigator = DualNavigator(place=place, thing=thing)
        redirect_url = navigator.url(place.parent_object, 'view')
        database.session.delete(place)
        database.session.commit()
        return redirect(redirect_url)
    else:
        return home_redirect()


@place_bp.route('/update/<int:place_id>/<int:thing_id>', methods=['GET', 'POST'])
@login_required
def place_update(place_id, thing_id):
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if place and thing and place.may_update(current_user):
        form = PlaceUpdateForm(obj=place)
        navigator = DualNavigator(place=place, thing=thing)
        redirect_url = navigator.url(place, 'view')
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(redirect_url)
        elif form.validate_on_submit():
            update_place_from_form(place, form)
            database.session.commit()
            return redirect(redirect_url)
        else:
            return CupboardDisplayContext().render_template(
                'pages/form_page.j2', form=form, form_title=f'Update {place.name}')
    else:
        return home_redirect()
