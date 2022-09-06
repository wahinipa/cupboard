#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask import current_app, request, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from tracking.commons.blueprint_registration import ADMIN_URL, HOME_PAGE_URL


def request_info(prefix):
    url = request.url
    try:
        username = current_user.username if current_user else 'NO USER'
    except AttributeError:
        username = 'Anonymous'
    route = request.access_route
    when = datetime.now()
    return f'{prefix}: {url} requested by {username} at {when} via {route}'


def log_info_about_request(prefix):
    current_app.logger.info(request_info(prefix))


def log_warn_about_request(prefix):
    current_app.logger.warning(request_info(prefix))


def redirect_hacks():
    log_warn_about_request('Redirect Hack')
    return redirect((url_for('fake_bp.fake')))


def initialize_database(database):
    database.create_all()  # Create sql tables for our data models
    from tracking.people.people_models import create_initial_users
    create_initial_users()
    database.session.commit()


def add_flask_admin(application, database):
    admin = Admin(application, 'Wonderful Trains', url=ADMIN_URL)
    admin.add_link(MenuLink(name='Home Page', url=HOME_PAGE_URL))
    # Using local imports helps break circularity of dependencies
    from tracking.people.people_models import User
    from tracking.groups.group_models import Group
    from tracking.places.place_models import Place
    from tracking.things.thing_models import Thing
    from tracking.roles.role_models import Role
    from tracking.roles.role_models import Assignment
    admin.add_view(UserAdminModelView(User, database.session))
    admin.add_view(AdminModelView(Assignment, database.session))
    admin.add_view(AdminModelView(Group, database.session))
    admin.add_view(AdminModelView(Place, database.session))
    admin.add_view(AdminModelView(Role, database.session))
    admin.add_view(AdminModelView(Thing, database.session))


class AdminModelView(ModelView):

    def is_accessible(self):
        from flask_login import current_user
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        from flask import url_for
        from flask import request
        return redirect(url_for('login', next=request.url))


class UserAdminModelView(AdminModelView):

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password)
