#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking import database
from tracking.commons.cupboard_navigation import create_cupboard_navigator
from tracking.forms.thing_forms import ThingUpdateForm, ThingCreateForm
from tracking.modelling.thing_model import find_thing_by_id
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect

thing_bp = Blueprint(
    'thing_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@thing_bp.route('/create/<int:thing_id>', methods=['POST', 'GET'])
@login_required
def thing_create(thing_id):
    thing = find_thing_by_id(thing_id)
    if thing is None or not thing.may_create_thing(current_user):
        return home_redirect()
    form = ThingCreateForm()
    navigator = DualNavigator(thing.root)
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(navigator.url(thing, 'view'))
    if form.validate_on_submit():
        new_thing = thing.create_kind_of_thing(name=form.name.data, description=form.description.data)
        return redirect(navigator.url(new_thing, 'view'))
    else:
        return thing.display_context(navigator, current_user).render_template('pages/form_page.j2', form=form,
                                                                              form_title=f'Create New Kind of '
                                                                                         f'{thing.name}')


@thing_bp.route('/delete/<int:thing_id>')
@login_required
def thing_delete(thing_id):
    thing = find_thing_by_id(thing_id)
    if thing is not None and thing.may_delete(current_user):
        navigator = create_cupboard_navigator()
        redirect_url = navigator.url(thing.parent_object, 'view')
        database.session.delete(thing)
        database.session.commit()
        return redirect(redirect_url)
    else:
        return home_redirect()


@thing_bp.route('/update/<int:thing_id>', methods=['GET', 'POST'])
@login_required
def thing_update(thing_id):
    thing = find_thing_by_id(thing_id)
    if thing and thing.may_update(current_user):
        form = thing_update_form(thing)
        navigator = create_cupboard_navigator()
        redirect_url = navigator.url(thing, 'view')
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(redirect_url)
        if form.validate_on_submit():
            update_thing_from_form(thing, form)
            database.session.commit()
            return redirect(redirect_url)
        else:
            return thing.display_context(navigator, current_user).render_template('pages/form_page.j2', form=form)
    else:
        return home_redirect()


def thing_update_form(thing):
    return ThingUpdateForm(obj=thing)


def update_thing_from_form(thing, form):
    form.populate_obj(thing)


@thing_bp.route('/view/<int:thing_id>')
@login_required
def thing_view(thing_id):
    thing = find_thing_by_id(thing_id)
    if thing is not None and thing.may_be_observed(current_user):
        navigator = create_cupboard_navigator()
        return thing.display_context(navigator, current_user, as_child=False, child_depth=1,
                                     child_link_label=f'Thing').render_template('pages/thing_view.j2')
    else:
        return home_redirect()
