#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures_for_testing import app, dunce, buffoon, bossy, DUNCE_ROLE_NAME, DUNCE_DESCRIPTION, DUNCE_DATE, \
    BUFFOON_ROLE_NAME, BUFFOON_DESCRIPTION, BUFFOON_DATE, BOSSY_ROLE_NAME, BOSSY_DESCRIPTION, BOSSY_DATE, \
    curly_stooge_user, moe_stooge_user, larry_stooge_user, knights_of_the_round_table, queens_of_the_round_table
from tracking.roles.role_models import assign_role, find_or_create_role


def _pycharm_please_keep_these_imports():
    return app, dunce, buffoon, bossy, dunce, buffoon, bossy, curly_stooge_user, \
           moe_stooge_user, larry_stooge_user, knights_of_the_round_table, queens_of_the_round_table


def test_role_creation(dunce, buffoon, bossy):
    assert dunce.name == DUNCE_ROLE_NAME
    assert dunce.description == DUNCE_DESCRIPTION
    assert dunce.date_created == DUNCE_DATE

    assert buffoon.name == BUFFOON_ROLE_NAME
    assert buffoon.description == BUFFOON_DESCRIPTION
    assert buffoon.date_created == BUFFOON_DATE

    assert bossy.name == BOSSY_ROLE_NAME
    assert bossy.description == BOSSY_DESCRIPTION
    assert bossy.date_created == BOSSY_DATE

def test_roles_are_unique(dunce):
    another_dunce = find_or_create_role(DUNCE_ROLE_NAME, DUNCE_DESCRIPTION, DUNCE_DATE)
    assert dunce == another_dunce


def test_role_assignment(knights_of_the_round_table, queens_of_the_round_table, dunce, buffoon, bossy,
                         curly_stooge_user, moe_stooge_user, larry_stooge_user):
    role_a = assign_role(knights_of_the_round_table, dunce, curly_stooge_user)
    assert role_a is not None
    assert role_a.person == curly_stooge_user
    assert role_a.group == knights_of_the_round_table
    assert role_a.role == dunce

    role_b = assign_role(queens_of_the_round_table, buffoon, curly_stooge_user)
    assert role_b is not None
    assert role_b.person == curly_stooge_user
    assert role_b.group == queens_of_the_round_table
    assert role_b.role == buffoon

    role_c = assign_role(knights_of_the_round_table, buffoon, moe_stooge_user)
    assert role_c is not None
    assert role_c.person == moe_stooge_user
    assert role_c.group == knights_of_the_round_table
    assert role_c.role == buffoon

    role_d = assign_role(knights_of_the_round_table, buffoon, larry_stooge_user)
    assert role_d is not None
    assert role_d.person == larry_stooge_user
    assert role_d.group == knights_of_the_round_table
    assert role_d.role == buffoon

    role_e = assign_role(knights_of_the_round_table, bossy, moe_stooge_user)
    assert role_e is not None
    assert role_e.person == moe_stooge_user
    assert role_e.group == knights_of_the_round_table
    assert role_e.role == bossy

    curly_assignments = curly_stooge_user.assignments
    assert len(curly_assignments) == 2
    assert role_a in curly_assignments
    assert role_b in curly_assignments

    moe_assignments = moe_stooge_user.assignments
    assert len(moe_assignments) == 2
    assert role_c in moe_assignments
    assert role_e in moe_assignments

    larry_assignments = larry_stooge_user.assignments
    assert len(larry_assignments) == 1
    assert role_d in larry_assignments

    queen_assignments = queens_of_the_round_table.assignments
    assert len(queen_assignments) == 1
    assert role_b in queen_assignments

    knight_assignments = knights_of_the_round_table.assignments
    assert len(knight_assignments) == 4
    assert role_a in knight_assignments
    assert role_b not in knight_assignments
    assert role_c in knight_assignments
    assert role_d in knight_assignments
    assert role_e in knight_assignments

    assert larry_stooge_user.has_role(knights_of_the_round_table, "Buffoon")
    assert knights_of_the_round_table.has_role(larry_stooge_user, "Buffoon")
    assert not larry_stooge_user.has_role(knights_of_the_round_table, "Dunce")
    assert not larry_stooge_user.has_role(knights_of_the_round_table, "NoSuchThing")
    assert not larry_stooge_user.has_role(queens_of_the_round_table, "Buffoon")

    assert not curly_stooge_user.has_role(knights_of_the_round_table, "Buffoon")
    assert curly_stooge_user.has_role(knights_of_the_round_table, "Dunce")
    assert curly_stooge_user.has_role(queens_of_the_round_table, "Buffoon")

    assert knights_of_the_round_table.has_role(moe_stooge_user, "Bossy")
    assert knights_of_the_round_table.has_role(moe_stooge_user, "Buffoon")
    assert not knights_of_the_round_table.has_role(moe_stooge_user, "Nope")






