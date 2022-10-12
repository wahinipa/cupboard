#  Copyright (c) 2022, Wahinipa LLC
from old_testing.fixtures_for_testing import BUCKET_DATE, BUCKET_DESCRIPTION, BUCKET_NAME, app, bucket, light_saber, \
    LIGHT_SABER_THING_NAME, \
    LIGHT_SABER_THING_DESCRIPTION, \
    LIGHT_SABER_THING_DATE
from tracking.things.old_thing_models import find_or_create_thing


def _pycharm_please_keep_these_imports():
    return app, light_saber, bucket


def test_thing_creation(light_saber, bucket):
    assert light_saber.name == LIGHT_SABER_THING_NAME
    assert light_saber.description == LIGHT_SABER_THING_DESCRIPTION
    assert light_saber.date_created == LIGHT_SABER_THING_DATE
    kind = light_saber.kind_of
    assert kind is not None
    assert kind.name == "Everything"
    assert light_saber in kind.kinds

    assert bucket.name == BUCKET_NAME
    assert bucket.description == BUCKET_DESCRIPTION
    assert bucket.date_created == BUCKET_DATE
    kind = bucket.kind_of
    assert kind is not None
    assert kind.name == "Everything"
    assert bucket in kind.kinds


def test_things_are_unique_by_name(light_saber):
    thing = find_or_create_thing(LIGHT_SABER_THING_NAME, LIGHT_SABER_THING_DESCRIPTION)
    assert thing is not None
    assert thing == light_saber