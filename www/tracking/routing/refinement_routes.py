#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint, url_for, request, redirect
from flask_login import login_required, current_user

refinement_bp = Blueprint(
    'refinement_bp', __name__,
    template_folder='templates',
    static_folder='static',
)

# @refinement_bp.route('/delete/<int:place_id>/<int:thing_id>')
# @login_required
# def root_delete(place_id, thing_id):
#     pass
