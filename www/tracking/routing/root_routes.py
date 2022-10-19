#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.commons.cupboard_display_context import CupboardDisplayContext
from tracking.commons.cupboard_navigation import create_cupboard_navigator
from tracking.forms.root_forms import RootCreateForm, create_root_from_form, RootUpdateForm
from tracking.modelling.category_models import Category, all_categories_display_context
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.root_model import find_root_by_id, all_root_display_context, Root
from tracking.modelling.thing_model import find_thing_by_id
from tracking.navigation.dual_navigator import DualNavigator
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
    navigator = DualNavigator()
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
        navigator = DualNavigator(root=root)
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
        navigator = DualNavigator(root=root)
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
    navigator = DualNavigator()
    return all_root_display_context(navigator, current_user).render_template("pages/home_page.j2", active_flavor="home")

@root_bp.route('/category_list/<int:root_id>')
@login_required
def root_category_list(root_id):
    root = find_root_by_id(root_id)
    if root is not None and root.may_be_observed(current_user):
        navigator = create_cupboard_navigator()
        return all_categories_display_context(root, navigator, current_user).render_template("pages/category_list.j2")
    return home_redirect()


@root_bp.route('/view/<int:root_id>/<int:place_id>/<int:thing_id>')
@login_required
def root_view(root_id, place_id, thing_id):
    root = find_root_by_id(root_id)
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if root is not None and root.may_be_observed(current_user):
        if place is not None and place.root == root and place.may_be_observed(current_user):
            if thing is not None and thing.root == root and thing.may_be_observed(current_user):
                navigator = DualNavigator(root=root, place=place, thing=thing)
                category_list_url = navigator.url(root, 'category_list')
                return root.display_context(navigator, current_user, as_child=False, child_depth=2,
                                            children=[place, thing]).render_template('pages/root_view.j2',
                                                                                     category_list_url=category_list_url)
    return home_redirect()
