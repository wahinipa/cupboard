#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime
from os import environ

from flask import current_app, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user
from werkzeug.utils import redirect

from tracking.navigation.blueprint_registration import ADMIN_URL, HOME_PAGE_URL
from tracking.commons.create_test_data import create_test_data
from tracking.contexts.cupboard_display_context import project_name


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


def initialize_database(database):
    database.create_all()  # Create sql tables for our data models

    # Create Roles first, so initial users can be assigned roles.
    from tracking.modelling.role_models import find_or_create_standard_roles
    find_or_create_standard_roles()

    from tracking.modelling.people_model import create_initial_users
    initial_users = create_initial_users()


    if environ.get('ADD_TEST_DATA'):
        create_test_data(database, initial_users)

    database.session.commit()


def add_flask_admin(application, database):
    admin = Admin(application, project_name(), url=ADMIN_URL)
    admin.add_link(MenuLink(name='Home Page', url=HOME_PAGE_URL))
    # Using local imports helps break circularity of dependencies
    from tracking.modelling.people_model import User
    from tracking.modelling.category_model import Category
    from tracking.modelling.linkage_model import Linkage
    from tracking.modelling.place_model import Place
    from tracking.modelling.thing_model import Thing
    from tracking.modelling.choice_model import Choice
    from tracking.modelling.refinement_model import Refinement
    from tracking.modelling.root_model import Root
    from tracking.modelling.postioning_model import Positioning
    from tracking.modelling.role_models import RootAssignment
    from tracking.modelling.specification_model import Specification
    from tracking.modelling.role_models import UniversalAssignment
    from tracking.modelling.role_models import PlaceAssignment
    from tracking.modelling.role_models import Role
    admin.add_view(AdminModelView(Category, database.session))
    admin.add_view(AdminModelView(Choice, database.session))
    admin.add_view(AdminModelView(Place, database.session))
    admin.add_view(AdminModelView(Root, database.session))
    admin.add_view(AdminModelView(Thing, database.session))
    admin.add_view(AdminModelView(Positioning, database.session))
    admin.add_view(AdminModelView(Refinement, database.session))
    admin.add_view(AdminModelView(Specification, database.session))
    admin.add_view(AdminModelView(User, database.session))
    admin.add_view(AdminModelView(Linkage, database.session))
    admin.add_view(AdminModelView(UniversalAssignment, database.session))
    admin.add_view(AdminModelView(RootAssignment, database.session))
    admin.add_view(AdminModelView(PlaceAssignment, database.session))
    admin.add_view(AdminModelView(Role, database.session))


class AdminModelView(ModelView):

    def is_accessible(self):
        from flask_login import current_user
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        from flask import url_for
        from flask import request
        return redirect(url_for('login', next=request.url))
