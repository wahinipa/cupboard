# Copyright 2022 WillyMillsLLC
from flask import Blueprint

things_bp = Blueprint(
    'things_bp', __name__,
    template_folder='templates',
    static_folder='static',
)
