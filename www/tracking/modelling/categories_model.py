#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.cardistry_models import bread_crumbs
from tracking.navigation.root_holder import RootHolder
from tracking.viewing.cupboard_display_context import CupboardDisplayContextMixin


class Categories(RootHolder, CupboardDisplayContextMixin):
    flavor = 'categories'
    label = 'Categories'
    label_prefixes = {}
    singular_label = 'Categories'
    possible_tasks = ['create', 'view']

    @property
    def identities(self):
        return {'root_id': self.root.id, 'place_id': self.place.id, 'particular_thing_id':self.particular_thing_id.id}

    @property
    def name(self):
        return self.label

    @property
    def parent_object(self):
        return self.root

    @property
    def root_path(self):
        return [self.root, self]

    def viewable_children(self, viewer):
        return [category for category in self.root.sorted_categories if category.may_be_observed(viewer)]

    def add_description(self, context):
        pass

    def bread_crumbs(self, navigator):
        return bread_crumbs(navigator, [self.root, self], target=self)

    def may_perform_task(self, viewer, task):
        if task == 'view':
            return self.root.may_be_observed(viewer)
        elif task == 'create':
            return self.root.may_create_thing(viewer)
        else:
            return False
