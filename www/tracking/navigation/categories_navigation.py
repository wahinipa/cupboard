#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.role_models import Role
from tracking.viewers.categories_viewer import CategoriesViewer


def register_categories_navigation(navigator):
    def register(task, role_names):
        endpoint = f'categories_bp.categories_{task}'
        navigator.register(CategoriesViewer, task, endpoint, role_names)

    register('create', [Role.structuring_role_name, Role.super_role_name])
    register('view', [Role.structure_viewer_role_name, Role.structuring_role_name, Role.super_role_name])
