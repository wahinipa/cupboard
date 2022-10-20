#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for
from werkzeug.utils import redirect

from tracking.commons.administration import log_warn_about_request


def redirect_hackers():
    log_warn_about_request('Redirecting Hackers')
    return redirect((url_for('fake_bp.fake')))
