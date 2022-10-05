#  Copyright (c) 2022, Wahinipa LLC

from tracking.commons.pseudo_model import PseudoModel


class AllCategories(PseudoModel):
    def __init__(self, home):
        super().__init__(
            label="Categories",
            endpoint='category_bp.category_list',
            description="Categories are lists of Choices for being more specific about Things",
            parent_object=home
        )

    def may_be_observed(self, viewer):
        return viewer.may_observe_categories



class AllThings(PseudoModel):
    def __init__(self, home):
        super().__init__(
            label="Things",
            endpoint='thing_bp.thing_list',
            description="Things are inventory items that needs tracking",
            parent_object=home
        )

    def may_be_observed(self, viewer):
        return viewer.may_observe_things


class HomeModel(PseudoModel):
    def __init__(self):
        super().__init__(
            label='Home',
            endpoint='home_bp.home',
            description="Start Here",
            parent_object=None,
            classification="Root"
        )
        from tracking.groups.group_models import AllGroups
        from tracking.places.place_models import AllPlaces
        from tracking.people.people_models import AllPeople
        self.all_categories = AllCategories(self)
        self.all_groups = AllGroups(self)
        self.all_places = AllPlaces(self)
        self.all_people = AllPeople(self)
        self.all_things = AllThings(self)
        self._child_list = [
            self.all_groups,
            self.all_places,
            self.all_people,
            self.all_things,
            self.all_categories,
        ]

    def may_be_observed(self, viewer):
        return True

    @property
    def child_list(self):
        return self._child_list


home_root = HomeModel()
