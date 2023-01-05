#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.category_model import Category
from tracking.modelling.role_models import Role


def register_category_navigation(navigator):
    def register(task, role_names):
        endpoint = f'category_bp.category_{task}'
        navigator.register(Category, task, endpoint, role_names)

    register('create', [Role.structuring_role_name])
    register('delete', [Role.structuring_role_name])
    register('update', [Role.structuring_role_name])
    register('view', [Role.structure_viewer_role_name, Role.structuring_role_name])
    register('add', [Role.structuring_role_name, Role.super_role_name])
    register('remove', [Role.structuring_role_name, Role.super_role_name])
