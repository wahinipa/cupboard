#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking import database
from tracking.forms.root_forms import RootUpdateForm, update_root_from_form
from tracking.viewers.categories_model import Categories
from tracking.viewers.inventory_model import Inventory
from tracking.viewers.platter import create_platter
from tracking.viewers.roots_model import Roots
from tracking.routing.home_redirect import home_redirect
from tracking.contexts.card_display_attributes import dual_view_childrens_attributes
from tracking.contexts.cupboard_display_context import CupboardDisplayContext

root_bp = Blueprint(
    'root_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@root_bp.route('/delete/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_delete(place_id, thing_id, specification_id):
    platter = create_platter(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if platter.may_be_observed(current_user):
        root = platter.root
        if root and root.may_delete(current_user):
            navigator = platter.create_navigator()
            redirect_url = navigator.url(Roots, 'view')
            database.session.delete(root)
            database.session.commit()
            return redirect(redirect_url)
    return home_redirect()


@root_bp.route('/update/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['GET', 'POST'])
@login_required
def root_update(place_id, thing_id, specification_id):
    platter = create_platter(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if platter.may_be_observed(current_user):
        root = platter.root
        if root and root.may_update(current_user):
            navigator = platter.create_navigator()
            form = RootUpdateForm(obj=root)
            redirect_url = navigator.url(root, 'view')
            if request.method == 'POST' and form.cancel_button.data:
                return redirect(redirect_url)
            if form.validate_on_submit():
                update_root_from_form(root, form)
                database.session.commit()
                return redirect(redirect_url)
            else:
                return CupboardDisplayContext().render_template(
                    'pages/form_page.j2', form=form, form_title=f'Update {root.name}')
    return home_redirect()


@root_bp.route('/view/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_view(place_id, thing_id, specification_id):
    platter = create_platter(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if platter.may_be_observed(current_user):
        navigator = platter.create_navigator()
        children = [platter.place, platter.thing, platter.thing_specification, Inventory(platter)]
        display_attributes = {
            'children': children,
            'children_attributes': dual_view_childrens_attributes(thing=platter.thing),
        }
        place_url = navigator.url(platter.root, 'view')
        category_list_url = navigator.url(
            Categories(place=platter.place, thing=platter.thing, specification=platter.specification),
            'view')
        return platter.root.display_context(
            navigator, current_user, display_attributes).render_template(
            'pages/root_view.j2', category_list_url=category_list_url, place_url=place_url,
            active_flavor='place')
    return home_redirect()
