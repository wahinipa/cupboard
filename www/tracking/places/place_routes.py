# Copyright 2022 Wahinipa LLC
from flask import Blueprint

places_bp = Blueprint(
    'places_bp', __name__,
    template_folder='../templates',
    static_folder='static',
)
