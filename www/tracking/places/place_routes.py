# Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.commons.display_context import display_context
from tracking.places.place_forms import PlaceUpdateForm
from tracking.places.place_models import find_place_by_id

place_bp = Blueprint(
    'place_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@place_bp.route('/delete/<int:place_id>')
@login_required
def place_delete(place_id):
    place = find_place_by_id(place_id)
    if place is not None and place.user_may_delete(current_user):
        database.session.delete(place)
        database.session.commit()
        return redirect(url_for('place_bp.place_list'))
    else:
        return redirect_hacks()


@place_bp.route('/list')
@login_required
def place_list():
    return render_template(
        'place_list.j2',
        tab="place",
        places=current_user.viewable_places,
        **display_context()
    )


@place_bp.route('/update/<int:place_id>', methods=['GET', 'POST'])
@login_required
def place_update(place_id):
    place = find_place_by_id(place_id)
    if place and place.user_may_update(current_user):
        form = place_update_form(place)
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('place_bp.place_view', place_id=place_id))
        if form.validate_on_submit():
            update_place_from_form(place, form)
            database.session.commit()
            return redirect(url_for('place_bp.place_view', place_id=place.id))
        else:
            return render_template(
                'place_update.j2',
                form=form,
                form_title=f'Update {place.name}',
                tab="place", **display_context()
            )
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
    if place is not None and place.user_may_view(current_user):
        return render_template(
            'place_view.j2',
            tab="place",
            **place.display_context(current_user)
        )
    else:
        return redirect(url_for('home_bp.home'))
