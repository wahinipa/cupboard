#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, curly_stooge_user, knights_of_the_round_table, larry_stooge_user, moe_stooge_user, \
    queens_of_the_round_table


def _pycharm_please_keep_these_imports():
    return app, curly_stooge_user, moe_stooge_user, larry_stooge_user, knights_of_the_round_table, queens_of_the_round_table


def test_linkage_assignment(knights_of_the_round_table, queens_of_the_round_table, curly_stooge_user, moe_stooge_user,
                            larry_stooge_user):
    assert len(knights_of_the_round_table.linkages) == 0
    assert len(queens_of_the_round_table.linkages) == 0
    assert len(queens_of_the_round_table.linkages) == 0
    assert len(curly_stooge_user.linkages) == 0
    assert len(moe_stooge_user.linkages) == 0
    assert len(larry_stooge_user.linkages) == 0

    assert not curly_stooge_user.is_linked(knights_of_the_round_table)
    curly_stooge_user.link_to_root(knights_of_the_round_table)
    assert curly_stooge_user.is_linked(knights_of_the_round_table)
    assert not curly_stooge_user.is_linked(queens_of_the_round_table)
    assert len(curly_stooge_user.linkages) == 1
    assert len(knights_of_the_round_table.linkages) == 1
    assert len(queens_of_the_round_table.linkages) == 0
    assert len(queens_of_the_round_table.linkages) == 0
    assert len(moe_stooge_user.linkages) == 0
    assert len(larry_stooge_user.linkages) == 0

    assert knights_of_the_round_table.is_linked(curly_stooge_user)
    assert not knights_of_the_round_table.is_linked(larry_stooge_user)

    assert curly_stooge_user.roots == [knights_of_the_round_table]

    # Testing duplicate does not happen
    curly_stooge_user.link_to_root(knights_of_the_round_table)
    assert curly_stooge_user.is_linked(knights_of_the_round_table)
    assert len(curly_stooge_user.linkages) == 1
    assert len(knights_of_the_round_table.linkages) == 1


def test_linkage_removal(knights_of_the_round_table, queens_of_the_round_table, curly_stooge_user, moe_stooge_user,
                            larry_stooge_user):
    curly_stooge_user.link_to_root(knights_of_the_round_table)
    assert curly_stooge_user.is_linked(knights_of_the_round_table)
    assert knights_of_the_round_table.is_linked(curly_stooge_user)

    curly_stooge_user.unlink_from_root(knights_of_the_round_table)
    assert not curly_stooge_user.is_linked(knights_of_the_round_table)
    assert not knights_of_the_round_table.is_linked(curly_stooge_user)
