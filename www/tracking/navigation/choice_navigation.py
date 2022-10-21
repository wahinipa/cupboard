#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.choice_model import Choice


def register_choice_navigation(navigator):
    def register(task):
        endpoint = f'choice_bp.choice_{task}'
        navigator.register(Choice, task, endpoint)

    register('delete')
    register('update')
    register('view')
