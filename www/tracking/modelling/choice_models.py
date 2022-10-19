#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask import url_for

from tracking import database
from tracking.commons.cupboard_display_context import CupboardDisplayContext
from tracking.modelling.base_models import NamedBaseModel


class Choice(NamedBaseModel):
    category_id = database.Column(database.Integer, database.ForeignKey('category.id'), nullable=False)
    # particulars = database.relationship('Particular', backref='choice', lazy=True, cascade='all, delete')

    @property
    def url(self):
        return url_for('choice_bp.choice_view', choice_id=self.id)

    @property
    def deletion_url(self):
        return url_for('choice_bp.choice_delete', choice_id=self.id)

    @property
    def url_update(self):
        return url_for('choice_bp.choice_update', choice_id=self.id)

    @property
    def parent_list(self):
        return self.category.parent_list + [self.category]

    def user_may_update(self, viewer):
        return self.category.user_may_update(viewer)

    def user_may_delete(self, viewer):
        return self.category.user_may_delete(viewer)

    def viewable_attributes(self, viewer, include_category_url=False):
        category_notation = {
            'label': 'Category',
            'value': self.category.name,
        }
        if include_category_url:
            category_notation['url'] = self.category.url
        attributes = {
            'classification': 'Choice',
            'name': self.name,
            'label': self.label,
            'view_url': self.url,
            'notations': [category_notation] + self.description_notation_list,
        }
        return attributes

    def display_context(self, viewer):
        choice_context = CupboardDisplayContext({
            'target': self.viewable_attributes(viewer, include_category_url=True),
            'label': self.label,
            'name': self.name,
            'parent_list': self.parent_list,
        })
        if viewer.may_update_choice:
            choice_context.add_action(self.url_update, self.name, 'update')
        if viewer.may_delete_choice:
            choice_context.add_action(self.deletion_url, self.name, 'delete')
        return choice_context

    def may_be_observed(self, viewer):
        return self.category.may_be_observed(viewer)


def find_or_create_choice(category, name, description="", date_created=None):
    choice = find_choice(category, name)
    if choice is None:
        if date_created is None:
            date_created = datetime.now()
        choice = Choice(category=category, name=name, description=description, date_created=date_created)
        database.session.add(choice)
        database.session.commit()
    return choice


def find_choice(category, name):
    return Choice.query.filter(Choice.category_id == category.id, Choice.name == name).first()


def find_choice_by_id(choice_id):
    return Choice.query.filter(Choice.id == choice_id).first()
