#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.root_model import Root


def register_root_navigation(navigator):

    def register(task):
        endpoint = f'root_bp.root_{task}'
        navigator.register(Root, task, endpoint)

    register('create')
    register('delete')
    register('list')
    register('update')
