#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, dunce, buffoon, bossy, rainbow_place, wild_place, curly_stooge_user, moe_stooge_user, \
    larry_stooge_user, knights_of_the_round_table, DUNCE_ROLE_NAME, DUNCE_DESCRIPTION, DUNCE_DATE, BUFFOON_ROLE_NAME, BUFFOON_DESCRIPTION, \
    BUFFOON_DATE, BOSSY_ROLE_NAME, BOSSY_DESCRIPTION, BOSSY_DATE, knights_of_the_round_table, queens_of_the_round_table
from tracking.modelling.role_models import assign_root_role, assign_place_role, assign_universal_role, \
    find_or_create_role, \
    find_or_create_standard_roles, find_role, Role


def _pycharm_please_keep_these_imports():
    return app, dunce, buffoon, bossy, dunce, buffoon, bossy, curly_stooge_user, moe_stooge_user, larry_stooge_user, \
           knights_of_the_round_table, rainbow_place, wild_place, queens_of_the_round_table


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


def test_root_role_reassignment(knights_of_the_round_table, queens_of_the_round_table, dunce, buffoon, bossy,
                                 curly_stooge_user, moe_stooge_user, larry_stooge_user):
    assert len(dunce.root_assignments) == 0
    role_a = assign_root_role(knights_of_the_round_table, dunce, curly_stooge_user)
    assert len(dunce.root_assignments) == 1
    role_b = assign_root_role(knights_of_the_round_table, dunce, curly_stooge_user)
    assert len(dunce.root_assignments) == 1
    assert role_a == role_b


def test_root_role_assignment(knights_of_the_round_table, queens_of_the_round_table, dunce, buffoon, bossy,
                               curly_stooge_user, moe_stooge_user, larry_stooge_user):
    assert len(dunce.root_assignments) == 0
    role_a = assign_root_role(knights_of_the_round_table, dunce, curly_stooge_user)
    assert role_a is not None
    assert role_a.person == curly_stooge_user
    assert role_a.root == knights_of_the_round_table
    assert role_a.role == dunce
    assert len(dunce.root_assignments) == 1
    assert role_a in dunce.root_assignments

    assert len(buffoon.root_assignments) == 0
    role_b = assign_root_role(queens_of_the_round_table, buffoon, curly_stooge_user)
    assert role_b in buffoon.root_assignments
    assert len(buffoon.root_assignments) == 1
    assert role_b is not None
    assert role_b.person == curly_stooge_user
    assert role_b.root == queens_of_the_round_table
    assert role_b.role == buffoon

    role_c = assign_root_role(knights_of_the_round_table, buffoon, moe_stooge_user)
    assert role_c is not None
    assert role_c.person == moe_stooge_user
    assert role_c.root == knights_of_the_round_table
    assert role_c.role == buffoon

    role_d = assign_root_role(knights_of_the_round_table, buffoon, larry_stooge_user)
    assert role_d is not None
    assert role_d.person == larry_stooge_user
    assert role_d.root == knights_of_the_round_table
    assert role_d.role == buffoon

    role_e = assign_root_role(knights_of_the_round_table, bossy, moe_stooge_user)
    assert role_e is not None
    assert role_e.person == moe_stooge_user
    assert role_e.root == knights_of_the_round_table
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


def test_place_role_assignment(rainbow_place, wild_place, dunce, buffoon, bossy,
                               curly_stooge_user, moe_stooge_user, larry_stooge_user):
    assert len(dunce.place_assignments) == 0
    role_a = assign_place_role(rainbow_place, dunce, curly_stooge_user)
    assert role_a is not None
    assert role_a.person == curly_stooge_user
    assert role_a.place == rainbow_place
    assert role_a.role == dunce
    assert len(dunce.place_assignments) == 1
    assert role_a in dunce.place_assignments

    assert len(buffoon.place_assignments) == 0
    role_b = assign_place_role(wild_place, buffoon, curly_stooge_user)
    assert role_b in buffoon.place_assignments
    assert len(buffoon.place_assignments) == 1
    assert role_b is not None
    assert role_b.person == curly_stooge_user
    assert role_b.place == wild_place
    assert role_b.role == buffoon

    role_c = assign_place_role(rainbow_place, buffoon, moe_stooge_user)
    assert role_c is not None
    assert role_c.person == moe_stooge_user
    assert role_c.place == rainbow_place
    assert role_c.role == buffoon

    role_d = assign_place_role(rainbow_place, buffoon, larry_stooge_user)
    assert role_d is not None
    assert role_d.person == larry_stooge_user
    assert role_d.place == rainbow_place
    assert role_d.role == buffoon

    role_e = assign_place_role(rainbow_place, bossy, moe_stooge_user)
    assert role_e is not None
    assert role_e.person == moe_stooge_user
    assert role_e.place == rainbow_place
    assert role_e.role == bossy

    curly_assignments = curly_stooge_user.place_assignments
    assert len(curly_assignments) == 2
    assert role_a in curly_assignments
    assert role_b in curly_assignments

    moe_assignments = moe_stooge_user.place_assignments
    assert len(moe_assignments) == 2
    assert role_c in moe_assignments
    assert role_e in moe_assignments

    larry_assignments = larry_stooge_user.place_assignments
    assert len(larry_assignments) == 1
    assert role_d in larry_assignments

    wild_place_assignments = wild_place.assignments
    assert len(wild_place_assignments) == 1
    assert role_b in wild_place_assignments

    rainbow_assignments = rainbow_place.assignments
    assert len(rainbow_assignments) == 4
    assert role_a in rainbow_assignments
    assert role_b not in rainbow_assignments
    assert role_c in rainbow_assignments
    assert role_d in rainbow_assignments
    assert role_e in rainbow_assignments

    assert larry_stooge_user.has_role(rainbow_place, "Buffoon")
    assert rainbow_place.has_role(larry_stooge_user, "Buffoon")
    assert not larry_stooge_user.has_role(rainbow_place, "Dunce")
    assert not larry_stooge_user.has_role(rainbow_place, "NoSuchThing")
    assert not larry_stooge_user.has_role(wild_place, "Buffoon")

    assert not curly_stooge_user.has_role(rainbow_place, "Buffoon")
    assert curly_stooge_user.has_role(rainbow_place, "Dunce")
    assert curly_stooge_user.has_role(wild_place, "Buffoon")

    assert rainbow_place.has_role(moe_stooge_user, "Bossy")
    assert rainbow_place.has_role(moe_stooge_user, "Buffoon")
    assert not rainbow_place.has_role(moe_stooge_user, "Nope")


def test_hierarchical_role_assignment(knights_of_the_round_table, rainbow_place, wild_place, dunce, buffoon, bossy,
                                      curly_stooge_user):
    assert len(curly_stooge_user.assignments) == 0

    role_a = assign_root_role(knights_of_the_round_table, dunce, curly_stooge_user)
    assert len(curly_stooge_user.assignments) == 1
    assert role_a in curly_stooge_user.root_assignments
    assert not curly_stooge_user.has_universal_role("Dunce")
    assert curly_stooge_user.has_role(knights_of_the_round_table, "Dunce")
    assert curly_stooge_user.has_role(rainbow_place, "Dunce")
    assert curly_stooge_user.has_role(wild_place, "Dunce")

    assert not curly_stooge_user.has_universal_role("Buffoon")
    assert not curly_stooge_user.has_role(knights_of_the_round_table, "Buffoon")
    assert not curly_stooge_user.has_role(rainbow_place, "Buffoon")
    assert not curly_stooge_user.has_role(wild_place, "Buffoon")
    role_b = assign_universal_role(buffoon, curly_stooge_user)
    assert len(curly_stooge_user.assignments) == 2
    assert curly_stooge_user.has_universal_role("Buffoon")
    assert curly_stooge_user.has_role(knights_of_the_round_table, "Buffoon")
    assert curly_stooge_user.has_role(rainbow_place, "Buffoon")
    assert curly_stooge_user.has_role(wild_place, "Buffoon")
    role_c = assign_universal_role(buffoon, curly_stooge_user)
    assert role_b == role_c



def test_standard_roles(app):
    standard_roles = {role.name: role for role in find_or_create_standard_roles()}
    for role_name in [
        "User Account Manager",
        "Organization Administrator",
        "Linking People",
        "Catalog Manager",
        "Inventory Manager",
        "Location Manager",
        "Observer",
        "Receiving Agent",
        "Shipping Agent",
        "Transfer Agent",
        "Auditing Agent",
    ]:
        assert standard_roles.get(role_name) is not None
