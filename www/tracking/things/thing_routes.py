# Copyright 2022 Wahinipa LLC
from flask import Blueprint

things_bp = Blueprint(
    'things_bp', __name__,
    template_folder='../templates',
    static_folder='static',
)
