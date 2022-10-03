#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.choices.choice_forms import ChoiceCreateForm, create_choice_from_form
from tracking.commons.display_context import display_context

choice_bp = Blueprint(
    'choice_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@choice_bp.route('/create', methods=['POST', 'GET'])
@login_required
def choice_create():
    if not current_user.can_create_choice:
        return redirect_hacks()
    form = choice_create_form()
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(url_for('choice_bp.choice_list'))
    if form.validate_on_submit():
        choice = create_choice_from_form(form)
        return redirect(url_for('choice_bp.choice_view', choice_id=choice.id))
    else:
        return render_template('choice_create.j2', form=form, tab="choice", **display_context())


def choice_create_form():
    return ChoiceCreateForm()


@choice_bp.route('/delete/<int:choice_id>')
@login_required
def choice_delete(choice_id):
    choice = find_choice_by_id(choice_id)
    if choice is not None and choice.user_may_delete(current_user):
        database.session.delete(choice)
        database.session.commit()
        return redirect(url_for('choice_bp.choice_list'))
    else:
        return redirect_hacks()


@choice_bp.route('/list')
@login_required
def choice_list():
    return render_template('choice_list.j2', tab="choice", **display_context())


@choice_bp.route('/update/<int:choice_id>', methods=['GET', 'POST'])
@login_required
def choice_update(choice_id):
    choice = find_choice_by_id(choice_id)
    if choice and choice.user_can_update(current_user):
        form = choice_update_form(choice)
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('choice_bp.choice_view', choice_id=choice_id))
        if form.validate_on_submit():
            update_choice_from_form(choice, form)
            database.session.commit()
            return redirect(url_for('choice_bp.choice_view', choice_id=choice.id))
        else:
            return render_template('choice_update.j2', form=form, tab="choice", **display_context())
    else:
        return redirect_hacks()


def choice_update_form(choice):
    ChoiceUpdateForm(choice)


def update_choice_from_form(choice, form):
    form.populate_obj(choice)


@choice_bp.route('/view/<int:choice_id>')
@login_required
def choice_view(choice_id):
    choice = find_choice_by_id(choice_id)
    if choice is not None and choice.user_may_view(current_user):
        return render_template('choice_view.j2', choice=choice, tab="choice", **display_context())
    else:
        return redirect(url_for('home_bp.home'))


