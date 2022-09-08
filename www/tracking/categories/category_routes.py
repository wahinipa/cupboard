#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint

category_bp = Blueprint(
    'category_bp', __name__,
    template_folder='../templates',
    static_folder='static',
)
