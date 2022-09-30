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
from tracking.commons.display_context import project_name


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

    from tracking.roles.role_models import find_or_create_standard_roles
    find_or_create_standard_roles()

    if environ.get('ADD_TEST_DATA'):
        create_test_data(database)

    database.session.commit()


def create_test_data(database):
    from tracking.things.thing_models import find_or_create_thing
    shoes = find_or_create_thing("Shoes", "Things to wear on your feet.")
    clothing = find_or_create_thing("Clothing", "Things to wear\nOr lose in the closet.")
    containers = find_or_create_thing("Containers", "Things to hold other things.")
    backpacks = find_or_create_thing("Backpacks", "Containers that\nStrap to your back.", kind_of=containers)
    gym_bags = find_or_create_thing("Gym Bags", description="", kind_of=containers)

    from tracking.categories.category_models import find_or_create_category
    sex_category = find_or_create_category("Sex", description="Whether for girls or boys or either.")
    seasonal_category = find_or_create_category("Season", description="Summer versus winter versus any season.")

    from tracking.choices.choice_models import find_or_create_choice
    sex_female = find_or_create_choice(sex_category, "Female", "For girl or woman.")
    sex_male = find_or_create_choice(sex_category, "Male", "For boy or man.")
    sex_any = find_or_create_choice(sex_category, "Either", "For either girl or boy.")
    seasonal_summer = find_or_create_choice(seasonal_category, "Summer", "Appropriate for summer.")
    seasonal_winter = find_or_create_choice(seasonal_category, "Winter", "Appropriate for winter.")
    seasonal_all_year = find_or_create_choice(seasonal_category, "All Year", "Appropriate for any season.")

    from tracking.categories.category_models import refine_thing
    clothing_by_season = refine_thing(clothing, seasonal_category)
    clothing_by_sex = refine_thing(clothing, sex_category)
    containers_by_sex = refine_thing(containers, sex_category)
    backpacks_by_season = refine_thing(backpacks, seasonal_category)

    from tracking.groups.group_models import find_or_create_group
    do_gooders = find_or_create_group("Do Gooders, Inc.", "Doing good\nwhile doing more good.")
    well_wishers = find_or_create_group("Society of Well Wishers",
                                        "If wishes were horses we would find you a pony.")

    from tracking.places.place_models import find_or_create_place
    out_back = find_or_create_place(do_gooders, "Out Back", "The shed behind the main office.\nClaudia has the key.")
    church_basement = find_or_create_place(well_wishers, "Church Basement", "")
    main_storage_unit = find_or_create_place(well_wishers, "Main Storage Unit", "Unit 17 at Store-Your-Stuff-Here")
    garage = find_or_create_place(well_wishers, "Garage", "Please keep locked when office is closed.")


def add_flask_admin(application, database):
    admin = Admin(application, project_name(), url=ADMIN_URL)
    admin.add_link(MenuLink(name='Home Page', url=HOME_PAGE_URL))
    # Using local imports helps break circularity of dependencies
    from tracking.people.people_models import User
    from tracking.categories.category_models import Category
    from tracking.choices.choice_models import Choice
    from tracking.groups.group_models import Group
    from tracking.roles.role_models import GroupAssignment
    from tracking.places.place_models import Place
    from tracking.roles.role_models import PlaceAssignment
    from tracking.positionings.postioning_models import Positioning
    from tracking.roles.role_models import Role
    from tracking.things.thing_models import Thing
    from tracking.roles.role_models import UniversalAssignment
    admin.add_view(AdminModelView(User, database.session))
    admin.add_view(AdminModelView(Group, database.session))
    admin.add_view(AdminModelView(GroupAssignment, database.session))
    admin.add_view(AdminModelView(Place, database.session))
    admin.add_view(AdminModelView(PlaceAssignment, database.session))
    admin.add_view(AdminModelView(Category, database.session))
    admin.add_view(AdminModelView(Choice, database.session))
    admin.add_view(AdminModelView(Positioning, database.session))
    admin.add_view(AdminModelView(Role, database.session))
    admin.add_view(AdminModelView(Thing, database.session))
    admin.add_view(AdminModelView(UniversalAssignment, database.session))


class AdminModelView(ModelView):

    def is_accessible(self):
        from flask_login import current_user
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        from flask import url_for
        from flask import request
        return redirect(url_for('login', next=request.url))
