#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user

from tracking.categories.category_models import find_category_by_id

category_bp = Blueprint(
    'category_bp', __name__,
    template_folder='../templates',
    static_folder='static',
)


@category_bp.route('/show/<int:category_id>')
@login_required
def show(category_id):
    category = find_category_by_id(category_id)
    if category is not None and category.user_may_view(current_user):
        return render_template('category_show.j2', category=category)
    else:
        return redirect(url_for('home_bp.home'))
