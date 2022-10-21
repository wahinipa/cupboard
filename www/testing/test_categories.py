#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, light_saber


# def _pycharm_please_keep_these_imports():
#     return app, pastry, light_saber, coloring
#
#
# def test_category_creation(pastry, coloring):
#     assert pastry is not None
#     assert pastry.name == PASTRY_NAME
#     assert pastry.description == PASTRY_DESCRIPTION
#     assert pastry.date_created == PASTRY_DATE
#
#     assert coloring is not None
#     assert coloring.name == COLORING_NAME
#     assert coloring.description == COLORING_DESCRIPTION
#     assert coloring.date_created == COLORING_DATE
#
#
# def test_refinement(light_saber, pastry):
#     refinement = refine_thing(light_saber, pastry)
#     assert refinement is not None
#     assert refinement.thing == light_saber
#     assert refinement.category == pastry
#     assert refinement in light_saber.refinements
#     assert refinement in pastry.refinements
#
#     another_refinement = refine_thing(light_saber, pastry)
#     assert another_refinement == refinement
#
#     light_saber_categories = light_saber.categories
#     assert len(light_saber_categories) == 1
#     assert light_saber_categories[0] == pastry
