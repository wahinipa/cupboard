# Copyright 2022 WillyMillsLLC
from flask import Blueprint

group_bp = Blueprint(
    'group_bp', __name__,
    template_folder='templates',
    static_folder='static',
)
