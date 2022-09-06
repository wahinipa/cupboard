# Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint

group_bp = Blueprint(
    'group_bp', __name__,
    template_folder='../templates',
    static_folder='static',
)
