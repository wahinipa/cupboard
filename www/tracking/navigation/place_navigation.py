#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.place_model import Place
from tracking.modelling.role_models import Role


def register_place_navigation(navigator):

    def register(task):
        endpoint = f'place_bp.place_{task}'
        navigator.register(Place, task, endpoint, [Role.location_manager_name, Role.super_role_name])

    register('create')
    register('delete')
    register('update')
