#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

from tracking.modelling.root_model import find_root_by_id, all_roots_display_context

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@home_bp.route('/')
def base():
    if current_user:
        return redirect(url_for('home_bp.home'))
    else:
        return redirect(url_for('people_bp.login'))


@home_bp.route('/home')
@login_required
def home():
    return all_roots_display_context(current_user).render_template()


@home_bp.route('/view/<int:root_id>')
@login_required
def root_view(root_id):
    root = find_root_by_id(root_id)
    if root is not None and root.may_be_observed(current_user):
        return root.display_context(current_user, as_child=False).render_template()
    else:
        return redirect(url_for('home_bp.home'))
