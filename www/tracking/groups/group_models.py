# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask import url_for

from tracking import database
from tracking.commons.base_models import ModelWithRoles, UniqueNamedBaseModel, name_is_key
from tracking.commons.display_context import DisplayContext
from tracking.commons.pseudo_model import PseudoModel


class AllGroups(PseudoModel):
    def __init__(self, home):
        super().__init__(
            label="Groups",
            endpoint='group_bp.group_list',
            description="Groups have Places which have Things",
            parent_object=home
        )

    def may_be_observed(self, viewer):
        return viewer.may_observe_groups

    @property
    def child_list(self):
        return sorted(Group.query.all(), key=name_is_key)

    def add_actions(self, context, viewer):
        if viewer.may_create_group:
            context.add_action(url_for('group_bp.group_create'), 'Group', 'create')
        return context.display_context


class Group(UniqueNamedBaseModel, ModelWithRoles):
    places = database.relationship('Place', backref='group', lazy=True, cascade='all, delete')
    group_assignments = database.relationship('GroupAssignment', backref='group', lazy=True, cascade='all, delete')

    @property
    def parent_list(self):
        from tracking.home.home_models import home_root
        return [home_root, home_root.all_groups]

    @property
    def sorted_places(self):
        return sorted(self.places, key=name_is_key)

    @property
    def assignments(self):
        return self.group_assignments

    @property
    def list_all_url(self):
        return url_for('group_bp.group_list')

    @property
    def url(self):
        return url_for('group_bp.group_view', group_id=self.id)

    @property
    def deletion_url(self):
        return url_for('group_bp.group_delete', group_id=self.id)

    @property
    def update_url(self):
        return url_for('group_bp.group_update', group_id=self.id)

    @property
    def place_create_url(self):
        return url_for('group_bp.place_create', group_id=self.id)

    def viewable_attributes(self, viewer):
        attributes = {
            'classification': 'Group',
            'name': self.name,
            'label': self.label,
            'view_url': self.url,
            'notations': self.description_notation,
        }
        return attributes

    def display_context(self, viewer):
        group_context = DisplayContext({
            'label': self.label,
            'target': self.viewable_attributes(viewer),
            'parent_list': self.parent_list,
            'children': [place.viewable_attributes(viewer, include_group_url=False) for place in self.sorted_places],
        })
        if self.user_may_create_place(viewer):
            group_context.add_action(self.place_create_url, f'Place for {self.name}', 'create')
        if viewer.may_update_group:
            group_context.add_action(self.update_url, self.name, 'update')
        if viewer.may_delete_group:
            group_context.add_action(self.deletion_url, self.name, 'delete')
        return group_context

    def may_be_observed(self, viewer):
        return True  # TODO: refine this

    def user_may_delete(self, user):
        return user.may_delete_group

    def user_may_update(self, user):
        return user.may_update_group

    def user_may_create_place(self, user):
        # TODO: refine this
        return user.may_update_group


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
