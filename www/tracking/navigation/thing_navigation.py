#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.thing_model import Thing


def register_thing_navigation(navigator):

    def register(task):
        endpoint = f'thing_bp.thing_{task}'
        navigator.register(Thing, task, endpoint)

    register('create')
    register('delete')
    register('update')
    register('view')
