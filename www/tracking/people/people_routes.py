# Copyright 2022 WillyMillsLLC
from flask import Blueprint

people_bp = Blueprint(
    'people_bp', __name__,
    template_folder='templates',
    static_folder='static',
)
