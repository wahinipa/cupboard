#  Copyright (c) 2022, Wahinipa LLC
from tracking import database
from tracking.modelling.base_models import DatedModelMixin, IdModelMixin


class Linkage(IdModelMixin, DatedModelMixin, database.Model):
    """
    Links a user to a Root object.

    Since most users will only link to one Root, the UI can eliminate
    unnecessary dialogs where the user chooses a root.
    """
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    root_id = database.Column(database.Integer, database.ForeignKey('root.id'))
