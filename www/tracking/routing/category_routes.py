#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from tracking.admin.administration import redirect_hacks
from tracking.forms.category_forms import CategoryCreateForm, CategoryUpdateForm
from tracking.forms.choice_forms import ChoiceCreateForm, create_choice_from_form
from tracking.modelling.category_models import find_category_by_id, Categories
from tracking.modelling.root_model import find_root_by_id
from tracking.navigation.dual_navigator import DualNavigator
from tracking.routing.home_redirect import home_redirect

category_bp = Blueprint(
    'category_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


# @category_bp.route('/create', methods=['POST', 'GET'])
# @login_required
# def category_create():
#     if not current_user.may_create_category:
#         return redirect_hacks()
#     form = category_create_form()
#     if request.method == 'POST' and form.cancel_button.data:
#         return redirect(url_for('category_bp.category_list'))
#     if form.validate_on_submit():
#         category = create_category_from_form(form)
#         return redirect(url_for('category_bp.category_view', category_id=category.id))
#     else:
#         return render_template('pages/form_page.j2', form=form, tab="category", **display_context())


def category_create_form():
    return CategoryCreateForm()


# @category_bp.route('/delete/<int:category_id>')
# @login_required
# def category_delete(category_id):
#     category = find_category_by_id(category_id)
#     if category is not None and category.user_may_delete(current_user):
#         database.session.delete(category)
#         database.session.commit()
#         return redirect(url_for('category_bp.category_list'))
#     else:
#         return redirect_hacks()


@category_bp.route('/view/<int:category_id>')
@login_required
def category_view(category_id):
    category = find_category_by_id(category_id)
    if category is not None and category.may_be_observed(current_user):
        navigator = DualNavigator()
        return category.display_context(navigator, current_user, as_child=False, child_depth=1).render_template(
            "pages/category_view.j2")
    else:
        return home_redirect()


@category_bp.route('/list/<int:root_id>')
@login_required
def category_list(root_id):
    root = find_root_by_id(root_id)
    if root is not None and root.may_be_observed(current_user):
        navigator = DualNavigator()
        categories = Categories(root)
        return categories.display_context(navigator, current_user, child_depth=1).render_template(
            "pages/category_list.j2")
    return home_redirect()


# @category_bp.route('/update/<int:category_id>', methods=['GET', 'POST'])
# @login_required
# def category_update(category_id):
#     category = find_category_by_id(category_id)
#     if category and category.user_may_update(current_user):
#         form = category_update_form(category)
#         if request.method == 'POST' and form.cancel_button.data:
#             return redirect(url_for('category_bp.category_view', category_id=category_id))
#         if form.validate_on_submit():
#             update_category_from_form(category, form)
#             database.session.commit()
#             return redirect(url_for('category_bp.category_view', category_id=category.id))
#         else:
#             return render_template('pages/form_page.j2', form=form, tab="category", **display_context())
#     else:
#         return redirect_hacks()


def category_update_form(category):
    return CategoryUpdateForm(category)


def update_category_from_form(category, form):
    form.populate_obj(category)


@category_bp.route('/create_choice/<int:category_id>', methods=['POST', 'GET'])
@login_required
def choice_create(category_id):
    category = find_category_by_id(category_id)
    if category and category.user_may_update(current_user):
        form = ChoiceCreateForm()
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('category_bp.category_view', category_id=category_id))
        if form.validate_on_submit():
            choice = create_choice_from_form(category, form)
            return redirect(url_for('choice_bp.choice_view', choice_id=choice.id))
        else:
            return render_template('pages/form_page.j2', form=form, form_title=f'Create new choice for {category.name}',
                                   tab="choice", **display_context())
    else:
        return redirect_hacks()
