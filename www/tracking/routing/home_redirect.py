#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for
from werkzeug.utils import redirect


def home_url():
    return url_for('root_bp.root_list')


def home_redirect():
    return redirect(home_url())
