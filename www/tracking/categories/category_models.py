#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database
from tracking.commons.base_models import UniqueNamedBaseModel


class Category(UniqueNamedBaseModel):
    pass


def find_or_create_category(name, description="", date_created=None):
    category = find_category_by_name(name)
    if category is None:
        if date_created is None:
            date_created = datetime.now()
        category = Category(name=name, description=description, date_created=date_created)
        database.session.add(category)
        database.session.commit()
    return category


def find_category_by_name(name):
    return Category.query.filter(Category.name == name).first()
