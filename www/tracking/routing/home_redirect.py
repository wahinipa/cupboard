#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for
from werkzeug.utils import redirect


def home_redirect():
    return redirect(url_for('home_bp.home'))