#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures_for_testing import app, bucket, coloring, light_saber, muffin, pastry, red_coloring, roll
from tracking.things.thing_models import find_or_create_particular_thing


def _pycharm_please_keep_these_imports():
    return app, pastry, muffin, roll, red_coloring, coloring, light_saber, bucket


def test_creating_particulars(pastry, muffin, roll, red_coloring, coloring, light_saber, bucket):
    particular_bucket = find_or_create_particular_thing(bucket, [red_coloring, muffin])
    assert particular_bucket is not None
    assert particular_bucket.thing == bucket
    assert particular_bucket in bucket.particular_things
    particular_bucket_choices = particular_bucket.choices
    assert particular_bucket_choices is not None
    assert len(particular_bucket_choices) == 2
    assert red_coloring in particular_bucket_choices
    assert muffin in particular_bucket_choices
    assert roll not in particular_bucket_choices
    assert particular_bucket in bucket.particular_things
    assert particular_bucket.thing == bucket
    assert particular_bucket.kind_of == bucket

    another_particular_bucket = find_or_create_particular_thing(bucket, [red_coloring, roll])
    assert another_particular_bucket is not None
    assert another_particular_bucket.thing == bucket
    assert another_particular_bucket in bucket.particular_things
    another_particular_bucket_choices = another_particular_bucket.choices
    assert another_particular_bucket_choices is not None
    assert len(another_particular_bucket_choices) == 2
    assert red_coloring in another_particular_bucket_choices
    assert muffin not in another_particular_bucket_choices
    assert roll in another_particular_bucket_choices

    repeat_particular_bucket = find_or_create_particular_thing(bucket, [red_coloring, muffin])
    assert repeat_particular_bucket == particular_bucket
