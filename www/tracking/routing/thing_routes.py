#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking import database
from tracking.forms.thing_forms import ThingUpdateForm, ThingCreateForm, update_thing_from_form
from tracking.viewers.platter import create_platter
from tracking.routing.home_redirect import home_redirect
from tracking.contexts.cupboard_display_context import CupboardDisplayContext

thing_bp = Blueprint(
    'thing_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@thing_bp.route('/create/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def thing_create(place_id, thing_id, specification_id):
    platter = create_platter(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if platter.may_be_observed(current_user) and platter.thing.may_create_thing(current_user):
        form = ThingCreateForm()
        navigator = platter.create_navigator()
        thing = platter.thing
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(navigator.url(thing, 'view'))
        if form.validate_on_submit():
            new_thing = thing.create_kind_of_thing(name=form.name.data, description=form.description.data)
            return redirect(navigator.url(new_thing, 'view'))
        else:
            return CupboardDisplayContext().render_template(
                'pages/form_page.j2', form=form, form_title=f'Create New Kind of {thing.name}')
    return home_redirect()


@thing_bp.route('/delete/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def thing_delete(place_id, thing_id, specification_id):
    platter = create_platter(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if platter.may_be_observed(current_user) and platter.thing.may_delete(current_user):
        navigator = platter.create_navigator()
        thing = platter.thing
        redirect_url = navigator.url(thing.parent_object, 'view')
        database.session.delete(thing)
        database.session.commit()
        return redirect(redirect_url)
    else:
        return home_redirect()


@thing_bp.route('/update/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['GET', 'POST'])
@login_required
def thing_update(place_id, thing_id, specification_id):
    platter = create_platter(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if platter.may_be_observed(current_user) and platter.thing.may_update(current_user):
        navigator = platter.create_navigator()
        thing = platter.thing
        form = ThingUpdateForm(obj=thing)
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
