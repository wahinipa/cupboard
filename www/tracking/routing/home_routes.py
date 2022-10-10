#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user

from tracking.commons.cupboard_display_context import CupboardDisplayContext
from tracking.modelling.root_model import all_roots

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
    context = CupboardDisplayContext(page_template="pages/home_page.j2")
    for root in all_roots():
        context.add_child_display_context(root.display_context(current_user))
    return context.render_template()
