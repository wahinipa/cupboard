# Copyright 2022 Wahinipa LLC
from testing.fixtures_for_testing import pretend_application
from tracking import blueprint_registration


def _pycharm_please_keep_these_imports():
    pretend_application


def test_registration(pretend_application):
    blueprint_registration(pretend_application)

    expected_blueprints = [
        'admin_bp',
        'fake_bp',
        'group_bp',
        'home_bp',
        'people_bp',
        'places_bp',
        'things_bp',
    ]
    for blueprint_name in expected_blueprints:
        blueprint_prefix = blueprint_name.split("_")[0]  # "things_bp" --> "things"
        registration = pretend_application.blueprints.get(blueprint_name)
        assert registration is not None
        blueprint = registration.get("blueprint")
        assert blueprint is not None
        assert blueprint.name == blueprint_name
        url_prefix = registration.get("url_prefix")
        assert url_prefix is not None
        if blueprint_name == 'fake_bp':
            assert url_prefix == "/"
        else:
            assert url_prefix.endswith(blueprint_prefix)
