#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime
from os import environ

from flask import current_app, request, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user
from werkzeug.utils import redirect

from tracking.commons.blueprint_registration import ADMIN_URL, HOME_PAGE_URL
from tracking.commons.cupboard_display_context import project_name


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


def redirect_hackers():
    log_warn_about_request('Redirecting Hackers')
    return redirect((url_for('fake_bp.fake')))


def initialize_database(database):
    database.create_all()  # Create sql tables for our data models

    from tracking.modelling.people_model import create_initial_users
    create_initial_users()

    # from tracking.roles.role_models import find_or_create_standard_roles
    # find_or_create_standard_roles()

    if environ.get('ADD_TEST_DATA'):
        create_test_data(database)

    database.session.commit()


def create_test_data(database):
    from tracking.modelling.root_model import create_root

    # Roots
    our_test_group = create_root(name="Our Test Group", description="For testing out the code.")
    another_test_group = create_root(name="Yet Another Test Group", description="For really, really testing out the code.\nLike, a lot.")

    # Places
    metropolis = our_test_group.place.create_kind_of_place(name="Metropolis", description="Home of the Daily Planet")
    smallville = our_test_group.place.create_kind_of_place(name="Smallville", description="Superboy's Home Town.\n Also, coincidentally, childhood home of Clark Kent.")
    phone_booth = smallville.create_kind_of_place(name="Phone Booth", description="Those tall boxes that had phones back in the day.")

    # Things
    shoes = our_test_group.thing.create_kind_of_thing("Shoes", "Things to wear on your feet.")
    clothing = our_test_group.thing.create_kind_of_thing("Clothing", "Things to wear\nOr lose in the closet.")
    containers = our_test_group.thing.create_kind_of_thing("Containers", "Things to hold other things.")
    backpacks = containers.create_kind_of_thing("Backpacks", "Containers that\nStrap to your back.")
    gym_bags = containers.create_kind_of_thing("Gym Bags", description="")

    # Categories
    our_test_group.create_category("Season", "Whether for summer or winter or either.")
    our_test_group.create_category("Sex", "Whether for girl or boy or either.")
    our_test_group.create_category("Age Appropriate", "Whether for infant, toddler, child, adult, or any.")


def add_flask_admin(application, database):
    admin = Admin(application, project_name(), url=ADMIN_URL)
    admin.add_link(MenuLink(name='Home Page', url=HOME_PAGE_URL))
    # Using local imports helps break circularity of dependencies
    from tracking.modelling.people_model import User
    from tracking.modelling.category_models import Category
    from tracking.modelling.place_model import Place
    from tracking.modelling.thing_model import Thing
    from tracking.modelling.choice_models import Choice
    from tracking.modelling.root_model import Root
    admin.add_view(AdminModelView(Category, database.session))
    admin.add_view(AdminModelView(Choice, database.session))
    admin.add_view(AdminModelView(Place, database.session))
    admin.add_view(AdminModelView(Root, database.session))
    admin.add_view(AdminModelView(Thing, database.session))
    admin.add_view(AdminModelView(User, database.session))


class AdminModelView(ModelView):

    def is_accessible(self):
        from flask_login import current_user
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        from flask import url_for
        from flask import request
        return redirect(url_for('login', next=request.url))
