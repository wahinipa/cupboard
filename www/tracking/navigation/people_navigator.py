#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.people_model import User


def register_people_navigation(navigator):

    def register(task):
        endpoint = f'people_bp.people_{task}'
        navigator.register(User, task, endpoint)

    register('create')
    register('delete')
    register('list')
    register('update')
    register('view')
