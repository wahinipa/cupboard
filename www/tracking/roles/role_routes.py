#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint

roles_bp = Blueprint(
    'roles_bp', __name__,
    template_folder='../templates',
    static_folder='static',
)
