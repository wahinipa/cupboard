#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.choice_model import Choice
from tracking.modelling.role_models import Role


def register_choice_navigation(navigator):
    def register(task, role_names):
        endpoint = f'choice_bp.choice_{task}'
        navigator.register(Choice, task, endpoint, role_names)

    register('delete', [Role.structuring_role_name])
    register('update', [Role.structuring_role_name])
    register('view', [Role.structure_viewer_role_name, Role.structuring_role_name])
