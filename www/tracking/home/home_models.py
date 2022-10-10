#  Copyright (c) 2022, Wahinipa LLC

from tracking.commons.pseudo_model import PseudoModel


class HomeModel(PseudoModel):
    def __init__(self):
        super().__init__(
            label='Home',
            endpoint='home_bp.home',
            description="Start Here",
            parent_object=None,
            classification="Root"
        )
        self._child_list = None
        from tracking.categories.category_models import AllCategories
        from tracking.groups.group_models import AllGroups
        from tracking.places.old_place_models import AllPlaces
        from tracking.people.people_models import AllPeople
        self.all_categories = AllCategories(self)
        self.all_groups = AllGroups(self)
        self.all_places = AllPlaces(self)
        self.all_people = AllPeople(self)
        self._all_things = None

    def may_be_observed(self, viewer):
        return True

    @property
    def all_things(self):
        if self._all_things is None:
            from tracking.things.old_thing_models import find_or_create_everything
            self._all_things = find_or_create_everything()
        return self._all_things

    @property
    def child_list(self):
        if self._child_list is None:
            self._child_list = [
                self.all_groups,
                self.all_places,
                self.all_people,
                self.all_things,
                self.all_categories,
            ]

        return self._child_list


home_root = HomeModel()
