#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, url_for, request, redirect
from flask_login import login_required, current_user

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.forms.root_forms import RootCreateForm, create_root_from_form, RootUpdateForm
from tracking.modelling.root_model import find_root_by_id, all_root_display_context, root_display_context

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
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(url_for('root_bp.root_list'))
    if form.validate_on_submit():
        root = create_root_from_form(form)
        return redirect(url_for('root_bp.root_view', root_id=root.id))
    else:
        return root_display_context(current_user).render_template(form=form, form_title="Create New Root")


@root_bp.route('/delete/<int:root_id>')
@login_required
def root_delete(root_id):
    root = find_root_by_id(root_id)
    if root is not None and root.may_delete(current_user):
        database.session.delete(root)
        database.session.commit()
        return redirect(url_for('root_bp.root_list'))
    else:
        return redirect_hacks()


@root_bp.route('/update/<int:root_id>', methods=['GET', 'POST'])
@login_required
def root_update(root_id):
    root = find_root_by_id(root_id)
    if root and root.may_update(current_user):
        form = RootUpdateForm(obj=root)
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('root_bp.root_view', root_id=root_id))
        if form.validate_on_submit():
            update_root_from_form(root, form)
            database.session.commit()
            return redirect(url_for('root_bp.root_view', root_id=root.id))
        else:
            return root.display_context(current_user).render_template('pages/form_page.j2', form=form, form_title=f'Update {root.name}')
    else:
        return redirect_hacks()


def update_root_from_form(root, form):
    form.populate_obj(root)


@root_bp.route('/list')
@login_required
def root_list():
    return all_root_display_context(current_user).render_template()


@root_bp.route('/view/<int:root_id>')
@login_required
def root_view(root_id):
    root = find_root_by_id(root_id)
    if root is not None and root.may_be_observed(current_user):
        return root.display_context(current_user, as_child=False).render_template('pages/root_view.j2')
    else:
        return redirect(url_for('home_bp.home'))
