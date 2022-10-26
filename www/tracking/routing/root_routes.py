#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking import database
from tracking.forms.root_forms import RootUpdateForm, update_root_from_form
from tracking.modelling.categories_model import Categories
from tracking.modelling.inventory_model import Inventory
from tracking.modelling.placement_model import create_placement
from tracking.modelling.roots_model import Roots
from tracking.routing.home_redirect import home_redirect
from tracking.viewing.card_display_attributes import dual_view_childrens_attributes
from tracking.viewing.cupboard_display_context import CupboardDisplayContext

root_bp = Blueprint(
    'root_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@root_bp.route('/delete/<int:place_id>/<int:thing_id>/<int:specification_id>')
@login_required
def root_delete(place_id, thing_id, specification_id):
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if placement.may_be_observed(current_user):
        root = placement.root
        if root and root.may_delete(current_user):
            navigator = placement.create_navigator()
            redirect_url = navigator.url(Roots, 'view')
            database.session.delete(root)
            database.session.commit()
            return redirect(redirect_url)
    return home_redirect()


@root_bp.route('/update/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['GET', 'POST'])
@login_required
def root_update(place_id, thing_id, specification_id):
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if placement.may_be_observed(current_user):
        root = placement.root
        if root and root.may_update(current_user):
            navigator = placement.create_navigator()
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
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if placement.may_be_observed(current_user):
        navigator = placement.create_navigator()
        children = [placement.place, placement.thing, placement.specification, Inventory(placement)]
        display_attributes = {
            'description': True,
            'children': children,
            'children_attributes': dual_view_childrens_attributes(),
        }
        place_url = navigator.url(placement.root, 'view')
        category_list_url = navigator.url(
            Categories(place=placement.place, thing=placement.thing, specification=placement.specification),
            'view')
        return placement.root.display_context(navigator, current_user, display_attributes).render_template(
            'pages/root_view.j2', category_list_url=category_list_url, place_url=place_url,
            active_flavor='place')
    return home_redirect()
