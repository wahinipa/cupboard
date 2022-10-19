#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.category_models import Category


def register_category_navigation(navigator):
    def register(task):
        endpoint = f'category_bp.category_{task}'
        navigator.register(Category, task, endpoint)

    register('choice_create')
    register('delete')
    register('update')
    register('view')
