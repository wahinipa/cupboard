#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint, url_for, request, redirect
from flask_login import login_required, current_user

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.commons.cupboard_navigation import create_cupboard_navigator
from tracking.forms.place_forms import PlaceCreateForm, PlaceUpdateForm
from tracking.modelling.place_model import find_place_by_id
from tracking.routing.home_redirect import home_redirect

place_bp = Blueprint(
    'place_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@place_bp.route('/create/<int:place_id>', methods=['POST', 'GET'])
@login_required
def place_create(place_id):
    place = find_place_by_id(place_id)
    if place is None or not place.may_create_place(current_user):
        return redirect_hacks()
    form = PlaceCreateForm()
    navigator = create_cupboard_navigator()
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(navigator.url(place, 'view'))
    if form.validate_on_submit():
        new_place = place.create_kind_of_place(name=form.name.data, description=form.description.data)
        return redirect(navigator.url(new_place, 'view'))
    else:
        return place.display_context(navigator, current_user).render_template("pages/form_page.j2", form=form,
                                                                   form_title=f'Create New Place for {place.name}')


@place_bp.route('/delete/<int:place_id>')
@login_required
def place_delete(place_id):
    place = find_place_by_id(place_id)
    if place is not None and place.may_delete(current_user):
        navigator = create_cupboard_navigator()
        redirect_url = navigator.url(place.parent_object, 'view')
        database.session.delete(place)
        database.session.commit()
        return redirect(redirect_url)
    else:
        return redirect_hacks()


@place_bp.route('/update/<int:place_id>', methods=['GET', 'POST'])
@login_required
def place_update(place_id):
    place = find_place_by_id(place_id)
    if place and place.may_update(current_user):
        form = place_update_form(place)
        navigator = create_cupboard_navigator()
        redirect_url = navigator.url(place, 'view')
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(redirect_url)
        if form.validate_on_submit():
            update_place_from_form(place, form)
            database.session.commit()
            return redirect(redirect_url)
        else:
            return place.display_context(navigator, current_user).render_template('pages/form_page.j2', form=form)
    else:
        return redirect_hacks()


def place_update_form(place):
    return PlaceUpdateForm(obj=place)


def update_place_from_form(place, form):
    form.populate_obj(place)


@place_bp.route('/view/<int:place_id>')
@login_required
def place_view(place_id):
    place = find_place_by_id(place_id)
    if place is not None and place.may_be_observed(current_user):
        navigator = create_cupboard_navigator()
        return place.display_context(navigator, current_user, as_child=False,
                                     child_link_label=f'Place').render_template('pages/place_view.j2')
    else:
        return home_redirect()
