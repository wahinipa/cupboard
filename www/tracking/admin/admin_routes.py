#  Copyright (c) 2022. Wahinipa LLC

from flask import Blueprint

admin_bp = Blueprint(
    'admin_bp', __name__,
    template_folder='../templates',
    static_folder='static',
)
