#  Copyright (c) 2022, Wahinipa LLC

category_display_attributes = {
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

dual_view_childrens_attributes = {
    'categories': categories_display_attributes,
    'category': category_display_attributes,
    'choice': choice_display_attributes,
    'place': place_display_attributes,
    'thing': thing_display_attributes,
}
