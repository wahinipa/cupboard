# Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.commons.display_context import display_context
from tracking.groups.group_forms import GroupCreateForm, create_group_from_form, GroupUpdateForm
from tracking.groups.group_models import find_group_by_id
from tracking.places.place_forms import PlaceCreateForm, create_place_from_form

group_bp = Blueprint(
    'group_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@group_bp.route('/create', methods=['POST', 'GET'])
@login_required
def group_create():
    if not current_user.may_create_group:
        return redirect_hacks()
    form = GroupCreateForm()
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(url_for('group_bp.group_list'))
    if form.validate_on_submit():
        group = create_group_from_form(form)
        return redirect(url_for('group_bp.group_view', group_id=group.id))
    else:
        return render_template('group_create.j2', form=form, tab="group", form_title='Create New Group', **display_context())


@group_bp.route('/delete/<int:group_id>')
@login_required
def group_delete(group_id):
    group = find_group_by_id(group_id)
    if group is not None and group.user_may_delete(current_user):
        database.session.delete(group)
        database.session.commit()
        return redirect(url_for('group_bp.group_list'))
    else:
        return redirect_hacks()


@group_bp.route('/list')
@login_required
def group_list():
    context = {}
    if current_user.may_create_group:
        context['create_group_url'] = url_for('group_bp.group_create')
    return render_template(
        'group_list.j2',
        tab="group",
        groups=current_user.viewable_groups,
        **display_context(context)
    )


@group_bp.route('/view/<int:group_id>')
@login_required
def group_view(group_id):
    group = find_group_by_id(group_id)
    if group and group.user_may_view(current_user):
        return render_template(
            'group_view.j2',
            tab="group",
            group=group.viewable_attributes(current_user, include_actions=True),
            **display_context()
        )
    else:
        return redirect(url_for('home_bp.home'))


@group_bp.route('/update/<int:group_id>', methods=['GET', 'POST'])
@login_required
def group_update(group_id):
    group = find_group_by_id(group_id)
    if group and group.user_may_update(current_user):
        form = group_update_form(group)
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('group_bp.group_view', group_id=group_id))
        if form.validate_on_submit():
            update_group_from_form(group, form)
            database.session.commit()
            return redirect(url_for('group_bp.group_view', group_id=group.id))
        else:
            return render_template('group_update.j2', form=form, tab="group", form_title=f'Update {group.name}', **display_context())
    else:
        return redirect_hacks()


def group_update_form(group):
    return GroupUpdateForm(obj=group)


def update_group_from_form(group, form):
    form.populate_obj(group)


@group_bp.route('/create_place/<int:group_id>', methods=['POST', 'GET'])
@login_required
def place_create(group_id):
    group = find_group_by_id(group_id)
    if group and group.user_may_update(current_user):
        form = PlaceCreateForm()
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('group_bp.group_view', group_id=group_id))
        if form.validate_on_submit():
            place = create_place_from_form(group, form)
            return redirect(url_for('place_bp.place_view', place_id=place.id))
        else:
            return render_template('place_create.j2', form=form, form_title=f'Create new place for {group.name}', tab="place", **display_context())
    else:
        return redirect_hacks()


