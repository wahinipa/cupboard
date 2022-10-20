#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for
from werkzeug.utils import redirect


def home_url():
    return url_for('roots_bp.roots_view')


def home_redirect():
    return redirect(home_url())
