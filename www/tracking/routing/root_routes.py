#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.commons.cupboard_display_context import CupboardDisplayContext
from tracking.commons.cupboard_navigation import create_cupboard_navigator
from tracking.forms.root_forms import RootCreateForm, create_root_from_form, RootUpdateForm
from tracking.modelling.root_model import find_root_by_id, all_root_display_context, Root
from tracking.routing.home_redirect import home_redirect

root_bp = Blueprint(
    'root_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@root_bp.route('/create', methods=['POST', 'GET'])
@login_required
def root_create():
    if not current_user.may_create_root:
        return redirect_hacks()
    form = RootCreateForm()
    navigator = create_cupboard_navigator()
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(navigator.url(Root, 'list'))
    if form.validate_on_submit():
        root = create_root_from_form(form)
        return redirect(navigator.url(root, 'view'))
    else:
        return CupboardDisplayContext().render_template("pages/form_page.j2", form=form, form_title="Create New Root")


@root_bp.route('/delete/<int:root_id>')
@login_required
def root_delete(root_id):
    root = find_root_by_id(root_id)
    if root is not None and root.may_delete(current_user):
        navigator = create_cupboard_navigator()
        database.session.delete(root)
        database.session.commit()
        return redirect(navigator.url(Root, 'list'))
    else:
        return redirect_hacks()


@root_bp.route('/update/<int:root_id>', methods=['GET', 'POST'])
@login_required
def root_update(root_id):
    root = find_root_by_id(root_id)
    if root and root.may_update(current_user):
        navigator = create_cupboard_navigator()
        form = RootUpdateForm(obj=root)
        redirect_url = navigator.url(root, 'view')
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(redirect_url)
        if form.validate_on_submit():
            update_root_from_form(root, form)
            database.session.commit()
            return redirect(redirect_url)
        else:
            return root.display_context(navigator, current_user).render_template('pages/form_page.j2', form=form,
                                                                                 form_title=f'Update {root.name}')
    else:
        return redirect_hacks()


def update_root_from_form(root, form):
    form.populate_obj(root)


@root_bp.route('/list')
@login_required
def root_list():
    navigator = create_cupboard_navigator()
    return all_root_display_context(navigator, current_user).render_template("pages/home_page.j2")


@root_bp.route('/view/<int:root_id>')
@login_required
def root_view(root_id):
    root = find_root_by_id(root_id)
    if root is not None and root.may_be_observed(current_user):
        navigator = create_cupboard_navigator()
        return root.display_context(navigator, current_user, as_child=False).render_template('pages/root_view.j2')
    else:
        return home_redirect()
