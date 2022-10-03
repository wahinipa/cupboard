#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required, current_user

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.categories.category_forms import CategoryCreateForm, CategoryUpdateForm, create_category_from_form
from tracking.categories.category_models import find_category_by_id
from tracking.choices.choice_forms import create_choice_from_form, ChoiceCreateForm
from tracking.commons.display_context import display_context, DisplayContext

category_bp = Blueprint(
    'category_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@category_bp.route('/create', methods=['POST', 'GET'])
@login_required
def category_create():
    if not current_user.can_create_category:
        return redirect_hacks()
    form = category_create_form()
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(url_for('category_bp.category_list'))
    if form.validate_on_submit():
        category = create_category_from_form(form)
        return redirect(url_for('category_bp.category_view', category_id=category.id))
    else:
        return render_template('category_create.j2', form=form, tab="category", **display_context())


def category_create_form():
    return CategoryCreateForm()


@category_bp.route('/delete/<int:category_id>')
@login_required
def category_delete(category_id):
    category = find_category_by_id(category_id)
    if category is not None and category.user_may_delete(current_user):
        database.session.delete(category)
        database.session.commit()
        return redirect(url_for('category_bp.category_list'))
    else:
        return redirect_hacks()


@category_bp.route('/list')
@login_required
def category_list():
    category_context = DisplayContext({
        'name': 'Categories',
        'categories': current_user.viewable_categories,
    })
    return render_template('category_list.j2', tab="category", **category_context.display_context)


@category_bp.route('/update/<int:category_id>', methods=['GET', 'POST'])
@login_required
def category_update(category_id):
    category = find_category_by_id(category_id)
    if category and category.user_can_update(current_user):
        form = category_update_form(category)
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('category_bp.category_view', category_id=category_id))
        if form.validate_on_submit():
            update_category_from_form(category, form)
            database.session.commit()
            return redirect(url_for('category_bp.category_view', category_id=category.id))
        else:
            return render_template('category_update.j2', form=form, tab="category", **display_context())
    else:
        return redirect_hacks()


def category_update_form(category):
    CategoryUpdateForm(category)


def update_category_from_form(category, form):
    form.populate_obj(category)


@category_bp.route('/view/<int:category_id>')
@login_required
def category_view(category_id):
    category = find_category_by_id(category_id)
    if category is not None and category.user_may_view(current_user):
        return render_template('category_view.j2', category=category, tab="category", **display_context())
    else:
        return redirect(url_for('home_bp.home'))


@category_bp.route('/create_choice/<int:category_id>', methods=['POST', 'GET'])
@login_required
def choice_create(category_id):
    category = find_category_by_id(category_id)
    if category and category.user_may_update(current_user):
        form = ChoiceCreateForm()
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('group_bp.group_view', category_id=category_id))
        if form.validate_on_submit():
            place = create_choice_from_form(category, form)
            return redirect(url_for('place_bp.place_view', place_id=place.id))
        else:
            return render_template('place_create.j2', form=form, form_title=f'Create new place for {category.name}',
                                   tab="place", **display_context())
    else:
        return redirect_hacks()
