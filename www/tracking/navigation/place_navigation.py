#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.place_model import Place


def register_place_navigation(navigator):

    def register(task):
        endpoint = f'place_bp.place_{task}'
        navigator.register(Place, task, endpoint)

    register('create')
    register('delete')
    register('update')
    register('view')
