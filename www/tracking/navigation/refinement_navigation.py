#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.refinement_model import Refinement


def register_refinement_navigation(navigator):
    def register(task):
        endpoint = f'refinement_bp.refinement_{task}'
        navigator.register(Refinement, task, endpoint)

    register('delete')
    register('create')
