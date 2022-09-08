#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database
from tracking.commons.base_models import BaseModel


class Choice(BaseModel):
    category_id = database.Column(database.Integer, database.ForeignKey('category.id'))
    particulars = database.relationship('Particular', backref='choice', lazy=True, cascade='all, delete')


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
