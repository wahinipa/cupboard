#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.category_models import Categories


def register_categories_navigation(navigator):
    def register(task):
        endpoint = f'categories_bp.categories_{task}'
        navigator.register(Categories, task, endpoint)

    register('create')
    register('view')
