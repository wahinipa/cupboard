# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database
from tracking.commons.base_models import UniqueNamedBaseModel, ModelWithRoles


class Group(UniqueNamedBaseModel, ModelWithRoles):
    places = database.relationship('Place', backref='group', lazy=True, cascade='all, delete')
    group_assignments = database.relationship('GroupAssignment', backref='group', lazy=True, cascade='all, delete')

    @property
    def assignments(self):
        return self.group_assignments


def find_or_create_group(name, description="", date_created=None):
    group = find_group_by_name(name)
    if group is None:
        if date_created is None:
            date_created = datetime.now()
        group = Group(name=name, description=description, date_created=date_created)
        database.session.add(group)
        database.session.commit()
    return group


def find_group_by_name(name):
    return Group.query.filter(Group.name == name).first()

def find_group_by_id(group_id):
    pass

