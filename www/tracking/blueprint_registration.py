# Copyright 2022 WillyMillsLLC

def my_url(url):
    from os import environ
    base_url = environ.get('BASE_URL', '/dev_testing')
    return f'{base_url}{url}'


GROUP_PREFIX = my_url('/group')
HOME_PREFIX = my_url('/home')
PEOPLE_PREFIX = my_url('/people')
PLACES_PREFIX = my_url('/places')
THINGS_PREFIX = my_url('/things')


def blueprint_registration(target_application):
    from www.tracking.home.home_routes import home_bp
    target_application.register_blueprint(home_bp, url_prefix=HOME_PREFIX)

    from www.tracking.groups.group_routes import group_bp
    target_application.register_blueprint(group_bp, url_prefix=GROUP_PREFIX)

    from www.tracking.people.people_routes import people_bp
    target_application.register_blueprint(people_bp, url_prefix=PEOPLE_PREFIX)

    from www.tracking.places.place_routes import places_bp
    target_application.register_blueprint(places_bp, url_prefix=PLACES_PREFIX)

    from www.tracking.things.thing_routes import things_bp
    target_application.register_blueprint(things_bp, url_prefix=THINGS_PREFIX)
