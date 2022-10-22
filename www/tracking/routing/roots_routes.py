#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking.forms.root_forms import RootCreateForm, create_root_from_form
from tracking.modelling.roots_model import Roots
from tracking.navigation.cupboard_navigation import create_cupboard_navigator
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect
from tracking.viewing.cupboard_display_context import CupboardDisplayContext

roots_bp = Blueprint(
    'roots_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@roots_bp.route('/create', methods=['POST', 'GET'])
@login_required
def roots_create():
    if not current_user.may_create_root:
        return home_redirect()
    form = RootCreateForm()
    navigator = create_cupboard_navigator()
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(navigator.url(Roots, 'view'))
    if form.validate_on_submit():
        root = create_root_from_form(form)
        return redirect(navigator.url(root, 'view'))
    else:
        return CupboardDisplayContext().render_template("pages/form_page.j2", form=form, form_title="Create New Root")


@roots_bp.route('/view')
@login_required
def roots_view():
    navigator = DualNavigator()
    roots = Roots()
    display_attributes = {
        'description': True,
        'url': True,
        'bread_crumbs': True,
        'children_attributes': {
            'root': {
                'display_context': {
                    'description': True,
                    'url': True,
                },
            },
        },
    }
    return roots.display_context(navigator, current_user, display_attributes).render_template("pages/home_page.j2",
                                                                                              active_flavor="home")
