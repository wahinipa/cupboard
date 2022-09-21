# Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, url_for, redirect, render_template
from flask_login import login_required, current_user

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.commons.display_context import display_context
from tracking.things.thing_models import find_thing_by_id

thing_bp = Blueprint(
    'thing_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@thing_bp.route('/create', methods=['POST', 'GET'])
@login_required
def thing_create():
    if not current_user.can_create_thing:
        return redirect_hacks()
    form = thing_create_form()
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(url_for('thing_bp.list'))
    if form.validate_on_submit():
        thing = create_thing_from_form(current_user, form)
        return redirect(url_for('thing_bp.thing_view', thing_id=thing.id))
    else:
        return render_template('thing_create_form.j2', form=form, tab="thing", **display_context())


def thing_create_form():
    pass


def create_thing_from_form(current_user, form):
    pass


@thing_bp.route('/delete/<int:thing_id>')
@login_required
def thing_delete(thing_id):
    thing = find_thing_by_id(thing_id)
    if thing is not None and thing.user_may_delete(current_user):
        database.session.delete(thing)
        database.session.commit()
        return redirect(url_for('thing_bp.thing_list'))
    else:
        return redirect_hacks()


@thing_bp.route('/list')
@login_required
def thing_list():
    return render_template('thing_list.j2', tab="thing")


@thing_bp.route('/update/<int:thing_id>', methods=['GET', 'POST'])
@login_required
def thing_update(thing_id):
    thing = find_thing_by_id(thing_id)
    if thing and thing.user_can_update(current_user):
        form = thing_update_form(thing)
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('thing_bp.thing_view', thing_id=thing_id))
        if form.validate_on_submit():
            update_thing_from_form(thing, form)
            database.session.commit()
            return redirect(url_for('thing_bp.thing_view', thing_id=thing.id))
        else:
            return render_template('thing_edit_form.j2', form=form, tab="thing", **display_context())
    else:
        return redirect_hacks()


def thing_update_form(thing):
    pass


def update_thing_from_form(thing, form):
    form.populate_obj(thing)


@thing_bp.route('/view/<int:thing_id>')
@login_required
def thing_view(thing_id):
    thing = find_thing_by_id(thing_id)
    if thing is not None and thing.user_may_view(current_user):
        return render_template('thing_view.j2', thing=thing, tab="thing", **display_context())
    else:
        return redirect(url_for('home_bp.home'))


