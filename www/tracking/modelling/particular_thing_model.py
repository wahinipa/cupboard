#  Copyright (c) 2022, Wahinipa LLC
from tracking import database
from tracking.modelling.base_models import IdModelMixin
from tracking.modelling.cardistry_models import bread_crumbs
from tracking.viewing.cupboard_display_context import CupboardDisplayContextMixin


class ParticularThing(IdModelMixin, CupboardDisplayContextMixin, database.Model):
    thing_id = database.Column(database.Integer, database.ForeignKey('thing.id'), index=True)
    specification_id= database.Column(database.Integer, database.ForeignKey('specification.id'), index=True)

    singular_label = "Particular Thing"
    plural_label = "Particular Things"
    possible_tasks = ['create', 'update', 'delete']
    label_prefixes = {'create': 'Kind of '}
    flavor = "thing"

    def add_description(self, context):
        return self.thing.add_description(context)

    @property
    def root_path(self):
        path = self.thing.root_path
        if not self.is_generic:
            path.append(self)
        return path

    @property
    def choice_label(self):
        choices = self.choices
        return (', ').join([f'{choice.name}' for choice in choices])

    def bread_crumbs(self, navigator):
        if self.is_generic:
            target = self.thing
        else:
            target = self
        return bread_crumbs(navigator, self.root_path, target=target)

    @property
    def label(self):
        return self.name

    @property
    def name(self):
        label = self.choice_label
        if label:
            return f'{label} {self.thing.name}'
        else:
            return self.thing.name

    @property
    def siblings(self):
        return self.thing.particular_things

    @property
    def is_generic(self):
        choices = self.choices
        return len(choices) == 0

    def has_choice(self, some_choice):
        for choice in self.choices:
            if choice.id == some_choice.id:
                return True
        return False

    def is_refinement(self, particular_thing):
        return self != particular_thing and self.thing == particular_thing.thing and self.has_refined_choices(
            particular_thing)

    def has_refined_choices(self, particular_thing):
        for choice in self.choices:
            if not particular_thing.has_choice(choice):
                return False
        return True

    @property
    def refinements(self):
        return [particular_thing for particular_thing in self.thing.particular_things if
                self.is_refinement(particular_thing)]

    @property
    def complete_refinements(self):
        return self.refinements + [self]

    def exact_quantity_at_place(self, place):
        from tracking.modelling.postioning_model import find_exact_quantity_of_things_at_place
        return find_exact_quantity_of_things_at_place(place, self.thing, self.specification)

    def exact_quantity_at_domain(self, place):
        return sum(self.exact_quantity_at_place(location) for location in place.complete_domain)

    def overall_quantity_at_place(self, place):
        return sum(refinement.exact_quantity_at_place(place) for refinement in self.complete_refinements)

    def overall_quantity_at_domain(self, place):
        return sum(self.overall_quantity_at_place(location) for location in place.complete_domain)

    def viewable_children(self, viewer):
        return self.thing.sorted_categories + self.refinements + self.thing.kinds

    @property
    def identities(self):
        return {'particular_thing_id': self.id}

    @property
    def kinds(self):
        return self.thing.kinds

    @property
    def kind_of(self):
        return self.thing

    @property
    def root(self):
        return self.thing.root

    @property
    def choices(self):
        return self.specification.choices

    def may_perform_task(self, viewer, task):
        return self.thing.may_perform_task(viewer, task)

    def may_be_observed(self, viewer):
        return self.thing.may_be_observed(viewer)

    def may_create_thing(self, viewer):
        return self.thing.may_create_thing(viewer)

    def may_delete(self, viewer):
        return self.thing.may_delete(viewer)

    def may_update(self, viewer):
        return self.thing.may_update(viewer)

    def add_to_place(self, place, quantity):
        from tracking.modelling.postioning_model import add_quantity_of_things
        return add_quantity_of_things(place, self.thing, self.specification, quantity)

    def find_particular(self, choice):
        for particular in self.particulars:
            if particular.choice == choice:
                return particular
        return None


def find_or_create_particular_thing(thing, choices=None):
    if choices is None:
        choices = set()
    else:
        choices = set(choices)  # Allow any iterable
    root = thing.root
    specification = root.find_or_create_specification(choices, commit=False)
    for some_particular_thing in specification.particular_things:
        if some_particular_thing.thing == thing:
            return some_particular_thing
    particular_thing = ParticularThing(thing=thing, specification=specification)
    database.session.add(particular_thing)
    database.session.commit()
    return particular_thing


def find_particular_thing_by_id(particular_thing_id):
    return ParticularThing.query.filter(ParticularThing.id == particular_thing_id).first()
