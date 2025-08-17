#  Copyright (c) 2022, Wahinipa LLC
# from testing.fixtures import app, light_saber, pastry, coloring, PASTRY_NAME, PASTRY_DESCRIPTION, PASTRY_DATE, \
#     COLORING_NAME, COLORING_DESCRIPTION, COLORING_DATE, knights_of_the_round_table, sharp_saber, dull_saber


from datetime import datetime
import pytest
# def _pycharm_please_keep_these_imports():
#     return app, pastry, light_saber, coloring, knights_of_the_round_table, sharp_saber, dull_saber
from tracking import create_app
@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        # if environ.get('TEST_SQL_IN_MEMORY') != 'True':
        #     basedir = path.abspath(path.dirname(__file__))
        #     test_data_base = path.join(basedir, 'cupboard_test.db')
        #     yield app
        #     remove(test_data_base)
        # else:
            yield app

def test_something():
    from testing.fixtures import app
    from tracking.modelling.root_model import create_root
    ROOT_NAME = "The Root"
    ROOT_DESCRIPTION = "Base Testing Object"

    ROUND_TABLE_DATE = datetime(1994, 6, 12)
    zzz = create_root(name=ROOT_NAME, description=ROOT_DESCRIPTION, date_created=ROUND_TABLE_DATE)
    assert zzz is not None


# def test_category_creation(knights_of_the_round_table, pastry, coloring):
#     assert pastry is not None
#     assert pastry.name == PASTRY_NAME
#     assert pastry.description == PASTRY_DESCRIPTION
#     assert pastry.date_created == PASTRY_DATE
#     assert pastry.root == knights_of_the_round_table
#
#     assert coloring is not None
#     assert coloring.name == COLORING_NAME
#     assert coloring.description == COLORING_DESCRIPTION
#     assert coloring.date_created == COLORING_DATE
#     assert coloring.root == knights_of_the_round_table
