#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint

role_bp = Blueprint(
    'role_bp', __name__,
    template_folder='../templates',
    static_folder='static',
)
