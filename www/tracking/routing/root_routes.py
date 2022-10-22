#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking import database
from tracking.forms.root_forms import RootUpdateForm, update_root_from_form
from tracking.modelling.categories_model import Categories
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.roots_model import Roots
from tracking.modelling.thing_model import find_thing_by_id
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect
from tracking.viewing.card_display_attributes import place_display_attributes, thing_display_attributes, \
    dual_view_childrens_attributes
from tracking.viewing.cupboard_display_context import CupboardDisplayContext

root_bp = Blueprint(
    'root_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@root_bp.route('/delete/<int:place_id>/<int:thing_id>')
@login_required
def root_delete(place_id, thing_id):
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if place and thing and place.root == thing.root:
        root = place.root
        if root and root.may_delete(current_user):
            navigator = DualNavigator(place=place, thing=thing)
            database.session.delete(root)
            database.session.commit()
            return redirect(navigator.url(Roots, 'view'))
    return home_redirect()


@root_bp.route('/update/<int:place_id>/<int:thing_id>', methods=['GET', 'POST'])
@login_required
def root_update(place_id, thing_id):
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if place and thing and place.root == thing.root:
        root = place.root
        if root and root.may_update(current_user):
            navigator = DualNavigator(place=place, thing=thing)
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


@root_bp.route('/view/<int:place_id>/<int:thing_id>')
@login_required
def root_view(place_id, thing_id):
    place = find_place_by_id(place_id)
    thing = find_thing_by_id(thing_id)
    if place and thing and place.root == thing.root:
        root = place.root
        if root and root.may_be_observed(current_user):
            if place and place.root == root and place.may_be_observed(current_user):
                if thing and thing.root == root and thing.may_be_observed(current_user):
                    navigator = DualNavigator(place=place, thing=thing)
                    display_attributes = {
                        'description': True,
                        'children': [place, thing],
                        'children_attributes': dual_view_childrens_attributes,
                    }
                    place_url = navigator.url(place.root, 'view')
                    category_list_url = navigator.url(Categories(place=place, thing=thing), 'view')
                    return root.display_context(navigator, current_user, display_attributes).render_template(
                        'pages/root_view.j2', category_list_url=category_list_url, place_url=place_url,
                        active_flavor='place')
    return home_redirect()
