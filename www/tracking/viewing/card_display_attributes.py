#  Copyright (c) 2022, Wahinipa LLC

def category_display_attributes(thing=None):
    attributes = {
        'display_context': {
            'description': True,
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
        'url': True,
        'bread_crumbs': True,
    }
}

place_display_attributes = {
    'display_context': {
        'description': True,
        'url': True,
        'bread_crumbs': True,
        'children_attributes': {
            'place': {
                'notation': True,
            },
        },
    }
}

thing_display_attributes = {
    'display_context': {
        'description': True,
        'url': True,
        'bread_crumbs': True,
        'children_attributes': {
            'category': {
                'notation': True,
            },
            'thing': {
                'notation': True,
            },
        },
    },
}

particular_thing_display_attributes = {
    'display_context': {
        'description': True,
        'url': True,
        'bread_crumbs': True,
        'children_attributes': {
            'category': {
                'notation': True,
            },
            'thing': {
                'notation': True,
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


def dual_view_childrens_attributes(thing=None):
    return {
        'categories': categories_display_attributes,
        'category': category_display_attributes(thing),
        'choice': choice_display_attributes,
        'inventory': inventory_display_attributes,
        'place': place_display_attributes,
        'thing': thing_display_attributes,
        'particular_thing': particular_thing_display_attributes,
    }
