#  Copyright (c) 2022, Wahinipa LLC
def my_url(url):
    from os import environ
    base_url = environ.get('BASE_URL', '/wahinipa')
    return f'{base_url}{url}'


ADMIN_URL = my_url('/admin')
HOME_PAGE_URL = my_url('/home')

CATEGORY_PREFIX = my_url('/category')
CATEGORIES_PREFIX = my_url('/categories')
CHOICE_PREFIX = my_url('/choice')
FAKE_PREFIX = '/'  # note: not using my_url
GROUP_PREFIX = my_url('/group')
HOME_PREFIX = my_url('/home')
USER_PREFIX = my_url('/people')
PLACES_PREFIX = my_url('/place')
REFINEMENT_PREFIX = my_url('/refinement')
ROLES_PREFIX = my_url('/role')
ROOT_PREFIX = my_url('/root')
ROOTS_PREFIX = my_url('/roots')
THINGS_PREFIX = my_url('/thing')


def blueprint_registration(application):
    # Using local imports helps break circularity of dependencies
    from tracking.routing.admin_routes import admin_bp
    application.register_blueprint(admin_bp, url_prefix=ADMIN_URL)

    from tracking.routing.home_routes import home_bp
    application.register_blueprint(home_bp, url_prefix=HOME_PREFIX)

    from tracking.routing.fake_routes import fake_bp
    application.register_blueprint(fake_bp, url_prefix=FAKE_PREFIX)

    from tracking.routing.category_routes import category_bp
    application.register_blueprint(category_bp, url_prefix=CATEGORY_PREFIX)

    from tracking.routing.categories_routes import categories_bp
    application.register_blueprint(categories_bp, url_prefix=CATEGORIES_PREFIX)

    from tracking.routing.choice_routes import choice_bp
    application.register_blueprint(choice_bp, url_prefix=CHOICE_PREFIX)

    from tracking.routing.people_routes import people_bp
    application.register_blueprint(people_bp, url_prefix=USER_PREFIX)

    from tracking.routing.refinement_routes import refinement_bp
    application.register_blueprint(refinement_bp, url_prefix=REFINEMENT_PREFIX)

    from tracking.routing.root_routes import root_bp
    application.register_blueprint(root_bp, url_prefix=ROOT_PREFIX)

    from tracking.routing.roots_routes import roots_bp
    application.register_blueprint(roots_bp, url_prefix=ROOTS_PREFIX)

    from tracking.routing.place_routes import place_bp
    application.register_blueprint(place_bp, url_prefix=PLACES_PREFIX)

    from tracking.routing.thing_routes import thing_bp
    application.register_blueprint(thing_bp, url_prefix=THINGS_PREFIX)
