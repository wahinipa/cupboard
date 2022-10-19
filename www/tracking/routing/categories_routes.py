#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking.commons.cupboard_display_context import CupboardDisplayContext
from tracking.forms.category_forms import CategoryCreateForm
from tracking.modelling.category_models import Categories
from tracking.modelling.root_model import find_root_by_id
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect

categories_bp = Blueprint(
    'categories_bp', __name__,
    template_folder='templates',
    static_folder='static',
)

@categories_bp.route('/create/<int:root_id>', methods=['POST', 'GET'])
@login_required
def categories_create(root_id):
    root = find_root_by_id(root_id)
    if root is not None and root.may_create_category(current_user):
        form = CategoryCreateForm()
        navigator = DualNavigator()
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(navigator.url(Categories(root), 'view'))
        if form.validate_on_submit():
            category = root.create_category(form.name.data, form.description.data)
            return redirect(navigator.url(category, 'view'))
        else:
            return CupboardDisplayContext().render_template('pages/form_page.j2', form=form, form_title=f'Create New Category for {root.name}')
    else:
        return home_redirect()


@categories_bp.route('/list/<int:root_id>')
@login_required
def categories_view(root_id):
    root = find_root_by_id(root_id)
    if root is not None and root.may_be_observed(current_user):
        navigator = DualNavigator()
        categories = Categories(root)
        return categories.display_context(navigator, current_user, child_depth=1).render_template(
            "pages/category_list.j2")
    return home_redirect()


