#  Copyright (c) 2022, Wahinipa LLC
def my_url(url):
    from os import environ
    base_url = environ.get('BASE_URL', '/wahinipa')
    return f'{base_url}{url}'


ADMIN_URL = my_url('/admin')
HOME_PAGE_URL = my_url('/home')

CATEGORY_PREFIX = my_url('/category')
FAKE_PREFIX = '/'  # note: not using my_url
GROUP_PREFIX = my_url('/group')
HOME_PREFIX = my_url('/home')
USER_PREFIX = my_url('/people')
PLACES_PREFIX = my_url('/places')
ROLES_PREFIX = my_url('/roles')
THINGS_PREFIX = my_url('/things')


def blueprint_registration(application):
    # Using local imports helps break circularity of dependencies
    from tracking.admin.admin_routes import admin_bp
    application.register_blueprint(admin_bp, url_prefix=ADMIN_URL)

    from tracking.categories.category_routes import category_bp
    application.register_blueprint(category_bp, url_prefix=CATEGORY_PREFIX)

    from tracking.home.fake_routes import fake_bp
    application.register_blueprint(fake_bp, url_prefix=FAKE_PREFIX)

    from tracking.groups.group_routes import group_bp
    application.register_blueprint(group_bp, url_prefix=GROUP_PREFIX)

    from tracking.home.home_routes import home_bp
    application.register_blueprint(home_bp, url_prefix=HOME_PREFIX)

    from tracking.people.people_routes import people_bp
    application.register_blueprint(people_bp, url_prefix=USER_PREFIX)

    from tracking.places.place_routes import places_bp
    application.register_blueprint(places_bp, url_prefix=PLACES_PREFIX)

    from tracking.roles.role_routes import roles_bp
    application.register_blueprint(roles_bp, url_prefix=ROLES_PREFIX)

    from tracking.things.thing_routes import things_bp
    application.register_blueprint(things_bp, url_prefix=THINGS_PREFIX)




