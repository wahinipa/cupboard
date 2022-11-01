#  Copyright (c) 2022, Wahinipa LLC

class ViewHandler:
    def validated_rendering(self):
        return self.display_context_maker.display_context(self.navigator, self.viewer,
                                                          self.display_attributes).render_template(
            self.page_template, category_list_url=self.category_list_url, place_url=self.place_url,
            active_flavor=self.active_flavor)

    @property
    def viewer_has_permission(self):
        return self.target.may_be_observed(self.viewer)
