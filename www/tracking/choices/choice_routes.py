#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint

choice_bp = Blueprint(
    'choice_bp', __name__,
    template_folder='templates',
    static_folder='static',
)
