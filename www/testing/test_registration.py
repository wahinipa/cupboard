# Copyright 2022 WillyMillsLLC
from www.testing.fixtures_for_testing import pretend_application
from www.tracking.blueprint_registration import blueprint_registeration


def _pycharm_please_keep_these_imports():
    pretend_application


def test_registration(pretend_application):
    blueprint_registeration(pretend_application)

    expected_blueprints = [
        'group_bp',
        'home_bp',
        'people_bp',
        'places_bp',
        'things_bp',
    ]
    for blueprint_name in expected_blueprints:
        registration = pretend_application.blueprints.get(blueprint_name)
        assert registration is not None
        blueprint = registration.get("blueprint")
        assert blueprint is not None
        assert blueprint.name == blueprint_name
