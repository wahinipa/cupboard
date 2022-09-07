# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database


class Group(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False, unique=True)
    description = database.Column(database.Text(), nullable=False, server_default='')
    date_created = database.Column(database.DateTime(), default=datetime.now())

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