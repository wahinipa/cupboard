#  Copyright (c) 2022, Wahinipa LLC

from tracking import database
from tracking.cardistry.models.cardistry_models import name_is_key
from tracking.commons.cupboard_display_context import CupboardDisplayContext, CupboardDisplayContextMixin
from tracking.modelling.base_models import UniqueNamedBaseModel


class Root(CupboardDisplayContextMixin, UniqueNamedBaseModel):
    singular_label = "Organizational Association"
    plural_label = "Organizational Associations"
    possible_tasks = ['update', 'delete']
    label_prefixes = {}

    place_id = database.Column(database.Integer, database.ForeignKey('place.id'), unique=True, nullable=False)
    thing_id = database.Column(database.Integer, database.ForeignKey('thing.id'), unique=True, nullable=False)

    @property
    def identities(self):
        return {'root_id': self.id}

    def may_perform_task(self, viewer, task):
        if task == 'view':
            return self.may_be_observed(viewer)
        elif task == 'delete':
            return self.may_delete(viewer)
        elif task == 'update':
            return self.may_update(viewer)
        elif task == 'create_place':
            return self.may_create_place(viewer)
        elif task == 'create_thing':
            return self.may_create_thing(viewer)
        else:
            return False

    def may_be_observed(self, viewer):
        return True

    def may_delete(self, viewer):
        return viewer.may_delete_root

    def may_create_place(self, viewer):
        return viewer.may_update_root

    def may_create_thing(self, viewer):
        return viewer.may_update_root

    def may_update(self, viewer):
        return viewer.may_update_root

    @property
    def parent_object(self):
        return None

    def viewable_children(self, viewer):
        if self.may_be_observed(viewer):
            return [self.place, self.thing]
        else:
            return []


def all_roots():
    return sorted(Root.query.all(), key=name_is_key)


def all_root_display_context(navigator, viewer):
    context = CupboardDisplayContext(label="Home")
    for root in all_roots():
        if root.may_be_observed(viewer):
            context.append_to_list('children', root.display_context(navigator, viewer))
    if viewer.may_create_root:
        context.add_task(navigator.url(Root, 'create'), label=Root.singular_label, task="create")
    return context


def create_root(name, description):
    from tracking.modelling.place_model import Place
    place_name = f'All of {name} Places'
    place_description = f'All of the top places for {name}'
    place = Place(name=place_name, description=place_description)
    database.session.add(place)

    from tracking.modelling.thing_model import Thing
    thing_name = f'All of {name} Things'
    thing_description = f'All of the top things for {name}'
    thing = Thing(name=thing_name, description=thing_description)
    database.session.add(thing)

    root = Root(name=name, description=description, place=place, thing=thing)
    database.session.add(root)
    database.session.commit()

    return root


def find_root_by_id(root_id):
    return Root.query.filter(Root.id == root_id).first()


def place_root(place):
    top = place.top
    return Root.query.filter(Root.place_id == top.id).first()


def thing_root(thing):
    top = thing.top
    return Root.query.filter(Root.thing_id == top.id).first()
