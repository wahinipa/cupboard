#  Copyright (c) 2022, Wahinipa LLC
def my_url(url):
    from os import environ
    base_url = environ.get('BASE_URL', '/wahinipa')
    return f'{base_url}{url}'


ADMIN_URL = my_url('/admin')
HOME_PAGE_URL = my_url('/home')

CATEGORY_PREFIX = my_url('/category')
CHOICE_PREFIX = my_url('/choice')
FAKE_PREFIX = '/'  # note: not using my_url
GROUP_PREFIX = my_url('/group')
HOME_PREFIX = my_url('/home')
USER_PREFIX = my_url('/people')
PLACES_PREFIX = my_url('/place')
ROLES_PREFIX = my_url('/role')
ROOT_PREFIX = my_url('/root')
THINGS_PREFIX = my_url('/thing')


def blueprint_registration(application):
    # Using local imports helps break circularity of dependencies
    from tracking.admin.admin_routes import admin_bp
    application.register_blueprint(admin_bp, url_prefix=ADMIN_URL)

    from tracking.routing.home_routes import home_bp
    application.register_blueprint(home_bp, url_prefix=HOME_PREFIX)

    from tracking.routing.people_routes import people_bp
    application.register_blueprint(people_bp, url_prefix=USER_PREFIX)

    from tracking.routing.route_routes import root_bp
    application.register_blueprint(root_bp, url_prefix=ROOT_PREFIX)

