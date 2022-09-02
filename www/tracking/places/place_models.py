# Copyright 2022 Wahinipa LLC
from datetime import datetime

from www.tracking.commons.builder import database


class Place(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    date_created = database.Column(database.DateTime(), default=datetime.now())
