# Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from tracking.home.home_models import home_root

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
    return home_root.display_context(current_user).render_template()
