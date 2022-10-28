#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.category_specification import CategorySpecification

def register_category_specification_navigation(navigator):
    endpoint = f'specification_bp.specification_update'
    # Actually does an update, but url generation defaults to 'view'
    navigator.register(CategorySpecification, 'view', endpoint)
