#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask import url_for

from tracking import database
from tracking.commons.base_models import BaseModel
from tracking.commons.display_context import DisplayContext


class Choice(BaseModel):
    category_id = database.Column(database.Integer, database.ForeignKey('category.id'))
    particulars = database.relationship('Particular', backref='choice', lazy=True, cascade='all, delete')

    @property
    def url(self):
        return url_for('choice_bp.choice_view', choice_id=self.id)

    @property
    def deletion_url(self):
        return url_for('choice_bp.choice_delete', choice_id=self.id)

    @property
    def update_url(self):
        return url_for('choice_bp.choice_update', choice_id=self.id)

    def viewable_attributes(self, viewer, include_category_url=False):
        attributes = {
            'name': self.name,
            'url': self.url,
            'lines': self.description_lines,
            'category_name': self.category.name,
        }
        if include_category_url:
            attributes['category_url'] = self.category.url
        return attributes

    def display_context(self, viewer):
        choice_context = DisplayContext({
            'choice': self.viewable_attributes(viewer, include_category_url=True),
            'name': self.name,
            'category_url': self.category.url,
            'parent_list': self.parent_list,
            'label': self.label
        })
        if viewer.may_update_choice:
            choice_context.add_action(self.update_url, self.name, 'update')
        if viewer.may_delete_choice:
            choice_context.add_action(self.deletion_url, self.name, 'delete')
        return choice_context.display_context



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