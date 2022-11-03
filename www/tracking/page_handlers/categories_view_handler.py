#  Copyright (c) 2022, Wahinipa LLC

from tracking.contexts.card_display_attributes import dual_view_childrens_attributes
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.active_platter_holding_handler import ActivePlatterHoldingHandler
from tracking.viewers.categories_model import Categories


class CategoriesViewHandler(PageHandler, ActivePlatterHoldingHandler):

    def __init__(self, viewer, **kwargs):
        PageHandler.__init__(self)
        ActivePlatterHoldingHandler.__init__(self, viewer, **kwargs)

    def validated_rendering(self):
        categories = Categories(place=self.place, thing=self.thing, specification=self.specification)
        display_attributes = {
            'description': True,
            'children': [categories, self.thing, self.thing_specification],
            'children_attributes': dual_view_childrens_attributes(),
        }
        place_url = self.navigator.url(self.root, 'view')
        category_list_url = self.navigator.url(categories, 'view')
        return self.root.display_context(self.navigator, self.viewer, display_attributes).render_template(
            "pages/category_list.j2", place_url=place_url, category_list_url=category_list_url,
            active_flavor='category')

    @property
    def viewer_has_permission(self):
        return self.platter.may_be_observed
