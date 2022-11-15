#  Copyright (c) 2022, Wahinipa LLC
from tracking.navigation.navigator import navigational_mark, navigational_identities, \
    navigator_registration_key, Navigator


class Fuzz:

    @property
    def identities(self):
        return {
            'bing': 1,
            'bang': 2,
            'buzz': 3,
        }


def test_navigational_mark():
    fuzz = Fuzz()
    assert navigational_mark(Fuzz) == 'Fuzz'
    assert navigational_mark(fuzz) == 'Fuzz'


def test_navigational_identities():
    fuzz = Fuzz()
    assert navigational_identities(Fuzz) == {}
    assert navigational_identities(fuzz) == {
        'bing': 1,
        'bang': 2,
        'buzz': 3,
    }


def test_navigator_registration_key():
    fuzz = Fuzz()
    assert navigator_registration_key(Fuzz, 'fiddle') == 'Fuzz:fiddle'
    assert navigator_registration_key(fuzz, 'faddle') == 'Fuzz:faddle'


def test_navigator():
    fuzz = Fuzz()
    navigator = Navigator()
    navigator.register(Fuzz, 'list', 'list_endpoint', ['rock', 'roll'])
    navigator.register(Fuzz, 'view', 'view_endpoint', ['zip', 'zap'])
    assert navigator.endpoint(Fuzz, 'list') == 'list_endpoint'
    assert navigator.endpoint(fuzz, 'list') == 'list_endpoint'
    assert navigator.endpoint(Fuzz, 'view') == 'view_endpoint'
    assert navigator.endpoint(fuzz, 'view') == 'view_endpoint'
    assert navigator.endpoint(Fuzz, 'nada') is None
    assert navigator.endpoint(fuzz, 'nada') is None
    assert navigator.endpoint_role_names('list_endpoint') == ['rock', 'roll']
    assert navigator.endpoint_role_names('view_endpoint') == ['zip', 'zap']
