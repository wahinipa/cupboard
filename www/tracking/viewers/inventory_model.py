#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.base_models import Descriptor
from tracking.modelling.positioning_mixin import filtered_positionings
from tracking.modelling.specification_model import describe_choices
from tracking.navigation.root_holder import RootHolder
from tracking.contexts.cupboard_display_context import CupboardDisplayContextMixin


class InventoryDescriptor(Descriptor):
    def __init__(self, label, name, quantity):
        super().__init__(flavor="inventory", label=label, name=name)
        self.quantity = quantity


class Inventory(RootHolder, CupboardDisplayContextMixin):
    flavor = "inventory"
    singular_label = 'Inventory'
    # 'ing' suffix makes these required tasks that show without needing a 'Show Actions' click
    possible_tasks = ['arriving', 'moving', 'departing']
    label_prefixes = {}

    def __init__(self, platter):
        super().__init__(place=platter.place, thing=platter.thing, specification=platter.specification)
        self.refinements = self.thing.refinements
        self.where_is_what = {self.place: self.specified_positionings(self.place.direct_positionings)}
        self.all_positioning = self.place.direct_positionings
        for place in self.place.places:
            positionings = self.specified_positionings(place.full_positionings)
            self.where_is_what[place] = positionings
            self.all_positioning |= positionings
        self.top_thing_set = self.thing.direct_set
        self.full_thing_set = self.thing.full_set
        self.full_place_set = self.place.full_set
        self.inventories = []
        self.described_choices = describe_choices(specification=self.specification)
        self.is_specific = platter.thing_specification.is_specific
        self.current_quantity = platter.current_quantity
        self.create_inventories()

    @property
    def identities(self):
        return {'place_id': self.place.id, 'thing_id': self.thing.id, 'specification_id': self.specification.id}

    def may_perform_task(self, viewer, task):
        # TODO: actually check on viewer
        if self.is_specific:
            return task == 'arriving' or self.current_quantity > 0
        else:
            return False

    def create_inventories(self):
        place_list = [self.place] + self.place.sorted_children
        thing_list = self.thing.sorted_children
        choice_list = self.specification.sorted_choices
        choices_insertion = f'{self.described_choices} for '

        def inventory_name(place, thing, quantity, insert='', choice_insert=None):
            if choice_insert is None:
                choice_insert = choices_insertion
            return f'{quantity} of {insert}{choice_insert}{thing.name} at {place.name}'

        total_quantity = 0
        for place in place_list:
            quantity = self.full_quantity_for_place(place)
            total_quantity += quantity
            name = inventory_name(place, self.thing, quantity)
            self.inventories.append(InventoryDescriptor("Place Count", name, quantity))

        for thing in thing_list:
            quantity = self.full_quantity_for_thing(thing)
            name = inventory_name(self.place, thing, quantity)
            self.inventories.append(InventoryDescriptor("Thing Count", name, quantity))

        for choice in choice_list:
            quantity = self.full_quantity_for_choice(choice)
            name = inventory_name(self.place, self.thing, quantity, choice_insert=f'{choice.name} ')
            self.inventories.append(InventoryDescriptor("Choice Count", name, quantity))

        self.inventories.append(
            InventoryDescriptor('Total', inventory_name(self.place, self.thing, total_quantity, insert='All '),
                                total_quantity))

    def specified_positionings(self, positionings):
        return {positioning for positioning in positionings if self.specification.accepts(positioning.specification)}

    def full_quantity_for_place(self, place):
        return sum(position.quantity for position in
                   filtered_positionings(self.where_is_what[place], things=self.full_thing_set))

    def full_quantity_for_choice(self, choice):
        return sum(position.quantity for position in
                   filtered_positionings(self.all_positioning, things=self.full_thing_set) if
                   position.specification.has_choice(choice))

    def full_quantity_for_thing(self, thing):
        return sum(position.quantity for position in
                   filtered_positionings(self.all_positioning, things=thing.direct_set))

    @property
    def quantity(self):
        return self.thing.quantity_at_place(self.place, self.specification)

    @property
    def name(self):
        return f'Quantities of {self.described_choices} for {self.thing.name} at {self.place.name}'

    def viewable_children(self, viewer):
        return [inventory for inventory in self.inventories if inventory.quantity]
