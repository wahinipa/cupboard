#  Copyright (c) 2022. Wahinipa LLC
def my_url(url):
    from os import environ
    base_url = environ.get('BASE_URL', '/wahinipa')
    return f'{base_url}{url}'


ADMIN_URL = my_url('/admin')
HOME_PAGE_URL = my_url('/home')

FAKE_PREFIX = '/'  # note: not using my_url
HOME_PREFIX = my_url('/')
USER_PREFIX = my_url('/users')


def blue_print_registration(application):
    # Using local imports helps break circularity of dependencies
    from tracking.home.home_routes import home_bp
    application.register_blueprint(home_bp, url_prefix=HOME_PREFIX)

    from tracking.people.people_routes import people_bp
    application.register_blueprint(people_bp, url_prefix=USER_PREFIX)
