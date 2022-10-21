#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking import database
from tracking.forms.thing_forms import ThingUpdateForm, ThingCreateForm, update_thing_from_form
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.thing_model import find_thing_by_id
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect
from tracking.viewing.cupboard_display_context import CupboardDisplayContext

thing_bp = Blueprint(
    'thing_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@thing_bp.route('/create/<int:place_id>/<int:thing_id>', methods=['POST', 'GET'])
@login_required
def thing_create(place_id, thing_id):
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if place and thing and place.root == thing.root is None or not thing.may_create_thing(current_user):
        return home_redirect()
    form = ThingCreateForm()
    navigator = DualNavigator(place=place, thing=thing)
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(navigator.url(thing, 'view'))
    if form.validate_on_submit():
        new_thing = thing.create_kind_of_thing(name=form.name.data, description=form.description.data)
        return redirect(navigator.url(new_thing, 'view'))
    else:
        return CupboardDisplayContext().render_template(
            'pages/form_page.j2', form=form, form_title=f'Create New Kind of {thing.name}')


@thing_bp.route('/delete/<int:place_id>/<int:thing_id>')
@login_required
def thing_delete(place_id, thing_id):
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if place and thing and place.root == thing.root is not None and thing.may_delete(current_user):
        navigator = DualNavigator(place=place, thing=thing)
        redirect_url = navigator.url(thing.parent_object, 'view')
        database.session.delete(thing)
        database.session.commit()
        return redirect(redirect_url)
    else:
        return home_redirect()


@thing_bp.route('/update/<int:place_id>/<int:thing_id>', methods=['GET', 'POST'])
@login_required
def thing_update(place_id, thing_id):
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if place and thing and place.root == thing.root and thing.may_update(current_user):
        form = ThingUpdateForm(obj=thing)
        navigator = DualNavigator(place=place, thing=thing)
        redirect_url = navigator.url(thing, 'view')
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(redirect_url)
        if form.validate_on_submit():
            update_thing_from_form(thing, form)
            database.session.commit()
            return redirect(redirect_url)
        else:
            return CupboardDisplayContext().render_template(
                'pages/form_page.j2', form=form, form_title=f'Update {thing.name}')
    else:
        return home_redirect()
