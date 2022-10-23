#  Copyright (c) 2022, Wahinipa LLC
from tracking.navigation.root_holder import RootHolder
from tracking.viewing.cupboard_display_context import CupboardDisplayContextMixin


class ParticularInventory:
    flavor = "inventory"
    singular_label = "Quantity"

    def __init__(self, place, particular_thing):
        self.place = place
        self.particular_thing = particular_thing
        self.quantity = self.particular_thing.total_quantity_at_place(self.place)

    @property
    def name(self):
        choices = self.particular_thing.choices
        if choices:
            choice_description = (', ').join([f'{choice.name}' for choice in choices])
        else:
            choice_description = 'Generic'
        return f'{self.quantity} of {choice_description} {self.particular_thing.thing.name}'

class TotalInventory:
    flavor = "inventory"

    def __init__(self, place, thing, singular_label='Total'):
        self.place = place
        self.thing = thing
        self.singular_label = singular_label
        self.quantity = self.thing.all_quantity_at_place(self.place)


    @property
    def name(self):
        return f'{self.quantity} of {self.thing.name} at {self.place.name}'


class Inventory(RootHolder, CupboardDisplayContextMixin):
    flavor = "inventory"
    singular_label = 'Inventory'
    possible_tasks = []

    def __init__(self, place, thing):
        super().__init__(place, thing)
        self.total_inventory = TotalInventory(self.place, self.thing, singular_label='Grand Total')
        particular_inventories = [ParticularInventory(self.place, particular_thing)
                for particular_thing in self.thing.all_particular_things]
        located_inventories = [TotalInventory(inner_place, self.thing, singular_label='Locale') for inner_place in self.place.places]
        inventories = particular_inventories + [self.total_inventory] + located_inventories
        self.inventories = [inventory for inventory in inventories if inventory.quantity]

    @property
    def quantity(self):
        return self.total_inventory.quantity

    @property
    def name(self):
        return f'Quantity of {self.thing.name} at {self.place.name}'

    def viewable_children(self, viewer):
        return self.inventories
