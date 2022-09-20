#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, request, render_template, redirect

from tracking.commons.display_context import display_context
from www.tracking.admin.administration import log_info_about_request, log_warn_about_request

fake_bp = Blueprint(
    'fake_bp', __name__,
    template_folder='../templates',
    static_folder='static',
)


@fake_bp.route('/')
def fake():
    log_info_about_request('Root Request')
    if 'wahinipa' not in request.host and '127.0.0.1' not in request.host and 'localhost' not in request.host:
        return rickroll()
    return render_template('fake_front.j2', **display_context())


# Find hacker urls with:
# cat /var/log/nginx/wahinipa.access.log | awk '{print $7}' | sort --unique


@fake_bp.endpoint("rickroll")
@fake_bp.route("/rickroll")
def rickroll(**kwargs):
    log_warn_about_request('Hacker Request')
    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


for rule in [
    '/MyAdmin/scripts/setup.php',
    '/PHPMYADMIN/scripts/setup.php',
    '/myadmin/scripts/setup.php',
    '/phpMyAdmin-2.10.0.2/scripts/setup.php',
    '/phpMyAdmin-2.10.1/scripts/setup.php',
    '/phpMyAdmin-2.10.3/scripts/setup.php',
    '/phpMyAdmin-2.11.1-rc1/scripts/setup.php',
    '/phpMyAdmin-2.11.10.1/scripts/setup.php',
    '/phpMyAdmin-2.11.11.3/scripts/setup.php',
    '/phpMyAdmin-2.11.11/scripts/setup.php',
    '/phpMyAdmin/scripts/setup.php',
    '/phpMyAdmin2/scripts/setup.php',
    '/phpMyadmin/scripts/setup.php',
    '/phpadmin/scripts/setup.php',
    '/phpmy/scripts/setup.php',
    '/phpmyadmin/scripts/setup.php',
    '/phpmyadmin2/scripts/setup.php',
    '/pma/scripts/setup.php',
    '/sql/scripts/setup.php',
    '/sqladmin/scripts/setup.php',
    '/ysqladmin/scripts/setup.php',
    '/.git/config',
    '/.env',
    '/Autodiscover/Autodiscover.xml',
    '/GponForm/diag_Formm',
    '/HNAP1',
    '/_ignition/execute-solution',
    '/_profile/phpinfo',
    '/ab2g',
    '/ab2h',
    '/admin/config.php',
    '/admin/jquery-file-upload/server/php/index.php',
    '/api/v1/ui_theme',
    '/cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh',
    '/config/getuser',
    '/console',
    '/dispatch.asp',
    '/doc/script/lib/seajs/config/sea-config.js',
    '/index.php',
    '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
    '/ecp/Current/exporttool/<junk>',
    '/owa/<junk>/<hunk>',
]:
    fake_bp.add_url_rule(rule, endpoint="rickroll")
