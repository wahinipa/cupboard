#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.category_model import Category


def register_refinement_navigation(navigator):
    def register(task):
        endpoint = f'refinement_bp.refinement_{task}'
        navigator.register(Category, task, endpoint)

    register('remove')
    register('add')
