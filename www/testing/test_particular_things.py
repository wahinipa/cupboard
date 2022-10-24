#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, pastry, muffin, roll, red_coloring, coloring, light_saber, bucket, knights_of_the_round_table
from tracking.modelling.particular_thing_model import find_or_create_particular_thing


def _pycharm_please_keep_these_imports():
    return app, pastry, muffin, roll, red_coloring, coloring, light_saber, bucket, knights_of_the_round_table


def test_creating_particulars(pastry, muffin, roll, red_coloring, coloring, light_saber, bucket, knights_of_the_round_table):
    particular_bucket = find_or_create_particular_thing(bucket, {red_coloring, muffin})
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

    another_particular_bucket = find_or_create_particular_thing(bucket, {red_coloring, roll})
    assert another_particular_bucket is not None
    assert another_particular_bucket.thing == bucket
    assert another_particular_bucket in bucket.particular_things
    another_particular_bucket_choices = another_particular_bucket.choices
    assert another_particular_bucket_choices is not None
    assert len(another_particular_bucket_choices) == 2
    assert red_coloring in another_particular_bucket_choices
    assert muffin not in another_particular_bucket_choices
    assert roll in another_particular_bucket_choices

    repeat_particular_bucket = find_or_create_particular_thing(bucket, {red_coloring, muffin})
    assert repeat_particular_bucket == particular_bucket


def test_generic(light_saber, knights_of_the_round_table):
    generic_light_saber = light_saber.generic
    assert generic_light_saber is not None
    assert len(generic_light_saber.choices) == 0
    another_generic = find_or_create_particular_thing(light_saber, set())
    assert another_generic == generic_light_saber
