#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

from tracking.modelling.root_model import all_root_display_context

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
    return all_root_display_context(current_user).render_template()
