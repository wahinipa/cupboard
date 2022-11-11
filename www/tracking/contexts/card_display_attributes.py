#  Copyright (c) 2022, Wahinipa LLC

def category_display_attributes(thing=None, **kwargs):
    attributes = {
        'display_context': {
            'description': True,
            'prefix': 'Category: ',
            'url': True,
            'bread_crumbs': True,
            'children_attributes': {
                'choice': {
                    'notation': True,
                },
            },
        },
    }
    if thing:
        attributes['display_context']['extra_action_parameters'] = {
            'thing': thing,
        }
    return attributes


categories_display_attributes = {
    'display_context': {
        'description': True,
        'prefix': 'Categories: ',
        'url': True,
        'bread_crumbs': True,
        'children_attributes': {
            'category': {
                'notation': True,
            },
        },
    }
}

choice_display_attributes = {
    'display_context': {
        'description': True,
        'prefix': 'Choice: ',
        'url': True,
        'bread_crumbs': True,
    }
}


def destination_display_attributes(destination_prefix=None, **kwargs):
    return {
        'display_context': {
            'description': True,
            'destination_quantity': True,
            'prefix': destination_prefix,
            'url': True,
            'bread_crumbs': True,
            'children_attributes': {
                'destination': {
                    'notation': True,
                    'destination_quantity': True,
                },
            },
        }
    }


def place_display_attributes(place_prefix=None, **kwargs):
    return {
        'display_context': {
            'source_quantity': True,
            'description': True,
            'prefix': place_prefix,
            'url': True,
            'bread_crumbs': True,
            'children_attributes': {
                'place': {
                    'notation': True,
                    'source_quantity' : True,
                },
            },
        }
    }


thing_display_attributes = {
    'display_context': {
        'description': True,
        'source_quantity': True,
        'url': True,
        'bread_crumbs': True,
        'children_attributes': {
            'thing': {
                'notation': True,
                'thing_quantity': True,
            },
        },
    },
}

inventory_display_attributes = {
    'display_context': {
        'children_attributes': {
            'inventory': {
                'notation': True,
            },
        },
    },
}

person_display_attributes = {
    'display_context': {
        'children_attributes': {
            'inventory': {
                'notation': True,
            },
        },
    },
}

specification_display_attributes = {
    'display_context': {
        'children_attributes': {
            'inventory': {
                'notation': True,
            },
            'category_specification': {
                'url': True,
                'notation': True,
            },
        },
    },
}


def dual_view_childrens_attributes(**kwargs):
    return {
        'categories': categories_display_attributes,
        'category': category_display_attributes(**kwargs),
        'choice': choice_display_attributes,
        'destination': destination_display_attributes(**kwargs),
        'inventory': inventory_display_attributes,
        'place': place_display_attributes(**kwargs),
        'specification': specification_display_attributes,
        'thing': thing_display_attributes,
        'person': person_display_attributes,
        'people': person_display_attributes,
    }
