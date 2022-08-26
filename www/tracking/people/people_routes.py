# Copyright 2022 Wahinipa LLC
from flask import Blueprint

people_bp = Blueprint(
    'people_bp', __name__,
    template_folder='templates',
    static_folder='static',
)
