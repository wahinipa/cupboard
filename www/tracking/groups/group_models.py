# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database
from tracking.commons.base_models import UniqueNamedBaseModel


class Group(UniqueNamedBaseModel):

    places = database.relationship('Place', backref='group', lazy=True, cascade='all, delete')
    assignments = database.relationship('Assignment', backref='group', lazy=True, cascade='all, delete')

    def has_role(self, person, name_of_role):
        for assignment in self.assignments:
            if assignment.person == person and assignment.role.name == name_of_role:
                return True
        return False


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
