#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, light_saber, bucket, LIGHT_SABER_THING_NAME, LIGHT_SABER_THING_DESCRIPTION, \
    LIGHT_SABER_THING_DATE, BUCKET_NAME, BUCKET_DESCRIPTION, BUCKET_DATE, the_root, ROOT_THING_NAME, \
    SHARP_SABER_THING_NAME, SHARP_SABER_THING_DESCRIPTION, SHARP_SABER_THING_DATE, sharp_saber, dull_saber


def _pycharm_please_keep_these_imports():
    return app, the_root, light_saber, bucket, sharp_saber, dull_saber


def test_thing_creation(light_saber, bucket, sharp_saber, dull_saber):
    assert light_saber.name == LIGHT_SABER_THING_NAME
    assert light_saber.description == LIGHT_SABER_THING_DESCRIPTION
    assert light_saber.date_created == LIGHT_SABER_THING_DATE
    kind = light_saber.kind_of
    assert kind is not None
    assert kind.name == ROOT_THING_NAME
    assert light_saber in kind.kinds

    assert bucket.name == BUCKET_NAME
    assert bucket.description == BUCKET_DESCRIPTION
    assert bucket.date_created == BUCKET_DATE
    kind = bucket.kind_of
    assert kind is not None
    assert kind.name == ROOT_THING_NAME
    assert bucket in kind.kinds

    assert sharp_saber.name == SHARP_SABER_THING_NAME
    assert sharp_saber.description == SHARP_SABER_THING_DESCRIPTION
    assert sharp_saber.date_created == SHARP_SABER_THING_DATE
    kind = sharp_saber.kind_of
    assert kind is not None
    assert kind.name == LIGHT_SABER_THING_NAME
    assert sharp_saber in kind.kinds
