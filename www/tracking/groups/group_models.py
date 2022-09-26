# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask import url_for

from tracking import database
from tracking.commons.base_models import ModelWithRoles, UniqueNamedBaseModel, name_is_key


class Group(UniqueNamedBaseModel, ModelWithRoles):
    places = database.relationship('Place', backref='group', lazy=True, cascade='all, delete')
    group_assignments = database.relationship('GroupAssignment', backref='group', lazy=True, cascade='all, delete')

    @property
    def assignments(self):
        return self.group_assignments

    @property
    def url(self):
        return url_for('group_bp.group_view', group_id=self.id)

    @property
    def deletion_url(self):
        return url_for('group_bp.group_delete', group_id=self.id)

    @property
    def update_url(self):
        return url_for('group_bp.group_update', group_id=self.id)

    def viewable_attributes(self, viewer, include_actions=False):
        attributes = {
            'name': self.name,
            'url': self.url,
            'lines': self.description_lines,
        }
        if include_actions:
            if viewer.can_delete_group:
                attributes['deletion_url'] = self.deletion_url
            if viewer.can_update_group:
                attributes['update_url'] = self.update_url
        return attributes

    def user_can_view(self, user):
        return True  # TODO: refine this

    def user_can_delete(self, user):
        return user.can_delete_group

    def user_can_update(self, user):
        return user.can_update_group


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
    return Group.query.filter(Group.id == group_id).first()


def all_groups():
    return sorted(Group.query.all(), key=name_is_key)
