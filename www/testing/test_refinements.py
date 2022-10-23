#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, light_saber, pastry, coloring, knights_of_the_round_table, sharp_saber, dull_saber
from tracking.modelling.refinement_model import add_refinement, remove_refinement


def _pycharm_please_keep_these_imports():
    return app, pastry, light_saber, coloring, knights_of_the_round_table, sharp_saber, dull_saber


def test_refinement(light_saber, sharp_saber, pastry, coloring, dull_saber):
    refinement = add_refinement(light_saber, pastry)
    assert refinement is not None
    assert refinement.thing == light_saber
    assert refinement.category == pastry
    assert refinement in light_saber.refinements
    assert refinement in pastry.refinements

    another_refinement = add_refinement(light_saber, pastry)
    assert another_refinement == refinement
    sharp_coloring_refinement = add_refinement(sharp_saber, coloring)

    light_saber_categories = light_saber.category_list
    assert len(light_saber_categories) == 1
    assert light_saber_categories[0] == pastry
    assert coloring not in light_saber_categories

    sharp_saber_categories = sharp_saber.category_list
    assert len(sharp_saber_categories) == 2
    assert pastry in sharp_saber_categories
    assert coloring in sharp_saber_categories

    light_saber_coloring_refinements = light_saber.category_refinements(coloring)
    assert light_saber_coloring_refinements is not None
    assert len(light_saber_coloring_refinements) == 1
    assert light_saber_coloring_refinements[0] == sharp_coloring_refinement

    sharp_saber_coloring_refinements = sharp_saber.category_refinements(coloring)
    assert sharp_saber_coloring_refinements is not None
    assert len(sharp_saber_coloring_refinements) == 1
    assert sharp_saber_coloring_refinements[0] == sharp_coloring_refinement

    dull_saber_coloring_refinements = dull_saber.category_refinements(coloring)
    assert dull_saber_coloring_refinements is not None
    assert len(dull_saber_coloring_refinements) == 0


def test_add_refinement(light_saber, sharp_saber, pastry, coloring, dull_saber):
    add_refinement(light_saber, pastry)
    add_refinement(sharp_saber, coloring)
    assert len(light_saber.refinements) == 1
    assert len(sharp_saber.refinements) == 1
    assert len(dull_saber.refinements) == 0

    assert len(light_saber.category_list) == 1
    assert len(sharp_saber.category_list) == 2
    assert len(dull_saber.category_list) == 1

    add_refinement(light_saber, coloring)
    assert len(light_saber.refinements) == 2
    assert len(sharp_saber.refinements) == 0
    assert len(dull_saber.refinements) == 0

    assert len(light_saber.category_list) == 2
    assert len(sharp_saber.category_list) == 2
    assert len(dull_saber.category_list) == 2

def test_remove_refinement(light_saber, sharp_saber, pastry, coloring, dull_saber):
    add_refinement(light_saber, pastry)
    assert len(light_saber.refinements) == 1
    assert len(sharp_saber.refinements) == 0
    assert len(dull_saber.refinements) == 0
    assert len(light_saber.category_list) == 1
    assert len(sharp_saber.category_list) == 1
    assert len(dull_saber.category_list) == 1

    remove_refinement(dull_saber, pastry)
    assert len(light_saber.refinements) == 0
    assert len(sharp_saber.refinements) == 1
    assert len(dull_saber.refinements) == 0
    assert len(light_saber.category_list) == 0
    assert len(sharp_saber.category_list) == 1
    assert len(dull_saber.category_list) == 0


