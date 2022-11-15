#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.category_model import Category
from tracking.modelling.role_models import Role


def register_refinement_navigation(navigator):
    def register(task):
        endpoint = f'refinement_bp.refinement_{task}'
        navigator.register(Category, task, endpoint, [Role.structuring_role_name, Role.super_role_name])

    register('remove')
    register('add')
