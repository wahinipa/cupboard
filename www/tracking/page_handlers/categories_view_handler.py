#  Copyright (c) 2022, Wahinipa LLC

from tracking.contexts.card_display_attributes import dual_view_childrens_attributes
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandlerMixin
from tracking.viewers.categories_model import Categories


class CategoriesViewHandler(PageHandler, PlatterHoldingHandlerMixin):

    def __init__(self, viewer, place_id, thing_id, specification_id):
        PageHandler.__init__(self)
        PlatterHoldingHandlerMixin.__init__(self, viewer, place_id=place_id, thing_id=thing_id,
                                            specification_id=specification_id)

    def validated_rendering(self):
        self.navigator = self.create_navigator()
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
