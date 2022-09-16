# Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint

thing_bp = Blueprint(
    'thing_bp', __name__,
    template_folder='../templates',
    static_folder='static',
)
