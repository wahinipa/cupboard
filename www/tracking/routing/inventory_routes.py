#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking.modelling.placement_model import create_placement
from tracking.routing.home_redirect import home_redirect
from tracking.viewing.cupboard_display_context import CupboardDisplayContext

inventory_bp = Blueprint(
    'inventory_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@inventory_bp.route('/arriving/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def inventory_arriving(place_id, thing_id, specification_id):
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if placement.may_be_observed(current_user) and placement.root.may_create_category(
        current_user):
        place = placement.place
        form = None  # InventoryArrivalForm()
        navigator = placement.create_navigator()
        redirect_url = navigator.url(placement.root, 'view')
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(redirect_url)
        if form.validate_on_submit():
            # category = place.root.create_category(form.name.data, form.description.data)
            return redirect(redirect_url)
        else:
            return CupboardDisplayContext().render_template('pages/form_page.j2', form=form,
                                                            form_title=f'Arrivals')
    else:
        return home_redirect()


@inventory_bp.route('/departing/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def inventory_departing(place_id, thing_id, specification_id):
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if placement.may_be_observed(current_user) and placement.root.may_create_category(
        current_user):
        place = placement.place
        form = None  # InventoryArrivalForm()
        navigator = placement.create_navigator()
        redirect_url = navigator.url(placement.root, 'view')
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(redirect_url)
        if form.validate_on_submit():
            # category = place.root.create_category(form.name.data, form.description.data)
            return redirect(redirect_url)
        else:
            return CupboardDisplayContext().render_template('pages/form_page.j2', form=form,
                                                            form_title=f'Arrivals')
    else:
        return home_redirect()


@inventory_bp.route('/moving/<int:place_id>/<int:thing_id>/<int:specification_id>', methods=['POST', 'GET'])
@login_required
def inventory_moving(place_id, thing_id, specification_id):
    placement = create_placement(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    if placement.may_be_observed(current_user) and placement.root.may_create_category(
        current_user):
        place = placement.place
        form = None  # InventoryArrivalForm()
        navigator = placement.create_navigator()
        redirect_url = navigator.url(placement.root, 'view')
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(redirect_url)
        if form.validate_on_submit():
            # category = place.root.create_category(form.name.data, form.description.data)
            return redirect(redirect_url)
        else:
            return CupboardDisplayContext().render_template('pages/form_page.j2', form=form,
                                                            form_title=f'Arrivals')
    else:
        return home_redirect()
