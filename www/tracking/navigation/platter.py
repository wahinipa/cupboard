#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for

from tracking.modelling.category_model import Category
from tracking.modelling.choice_model import Choice
from tracking.modelling.people_model import AllPeople, User, find_person_by_id
from tracking.modelling.place_model import Place, find_place_by_id
from tracking.modelling.positioning_mixin import current_quantity
from tracking.modelling.role_models import Role, find_role_by_id
from tracking.modelling.root_model import Root, find_root_by_id
from tracking.modelling.specification_model import find_specification_by_id
from tracking.modelling.thing_model import Thing, find_thing_by_id
from tracking.navigation.navigator import navigational_identities, navigational_mark
from tracking.viewers.Inventory_holder import create_inventory
from tracking.viewers.all_roles import AllRoles
from tracking.viewers.categories_viewer import CategoriesViewer
from tracking.viewers.category_specification_viewer import CategorySpecificationViewer
from tracking.viewers.destination import Destination
from tracking.viewers.roots_viewer import RootsViewer
from tracking.viewers.thing_specification_viewer import ThingSpecificationViewer

DEFAULT_ACTIVITY = 'observe'


class Platter:
    def __init__(self, viewer=None, activity=DEFAULT_ACTIVITY, root=None, place=None, thing=None, specification=None,
                 destination=None, person=None, role=None):
        self.viewer = viewer
        self.person = person
        self.role = role

        if self.role:
            self.role_id = self.role.id
        else:
            self.role_id = 0
        if root is None:
            if place:
                root = place.root
            elif thing:
                root = thing.root
            elif specification:
                root = specification.root
            elif destination:
                root = destination.root
        if root:
            place = place or root.place
            destination = destination or Destination(place)
            thing = thing or root.thing
            specification = specification or root.generic_specification
            self.root_id = root.id
        else:
            self.root_id = None

        if place:
            self.place_id = place.id
        else:
            self.place_id = None

        if person:
            self.person_id = person.id
        else:
            self.person_id = 0

        if destination:
            self.destination_id = destination.id
        else:
            self.destination_id = None

        if thing:
            self.thing_id = thing.id
        else:
            self.thing_id = None

        if specification:
            self.specification_id = specification.id
        else:
            self.specification_id = None

        self.activity = activity
        self.root = root
        self.place = place
        self.destination = destination
        self.thing = thing
        self.specification = specification

        self.source_inventory = create_inventory(self.place, self.thing, self.specification)
        self.destination_inventory = create_inventory(self.destination, self.thing, self.specification)

        from tracking.navigation.cupboard_navigation import create_cupboard_navigator
        self.navigator = create_cupboard_navigator()
        self.translator = {
            navigational_mark(CategoriesViewer): self.categories_url_maker,
            navigational_mark(Category): self.category_url_maker,
            navigational_mark(Choice): self.choice_url_maker,
            navigational_mark(Destination): self.destination_url_maker,
            navigational_mark(Place): self.place_url_maker,
            navigational_mark(Root): self.root_url_maker,
            navigational_mark(RootsViewer): self.roots_url_maker,
            navigational_mark(AllRoles): self.role_url_maker,
            navigational_mark(Role): self.role_url_maker,
            navigational_mark(CategorySpecificationViewer): self.specification_url_maker,
            navigational_mark(Thing): self.thing_url_maker,
            navigational_mark(ThingSpecificationViewer): self.thing_specification_url_maker,
            navigational_mark(AllPeople): self.user_url_maker,
            navigational_mark(User): self.user_url_maker,
        }
        self.viewer_role_name_set = set()
        if self.viewer:
            for role_name in Role.role_name_list + Role.pseudo_role_name_list:
                if self._viewer_has_role(role_name):
                    self.viewer_role_name_set.add(role_name)

    def default_url_maker(self, target, task, activity=None):
        endpoint = self.navigator.endpoint(target, task)
        if endpoint:
            identities = navigational_identities(target)
            return self.valid_url_for(endpoint, **identities)
        else:
            return None

    def categories_url_maker(self, categories, task, activity=None):
        return self.valid_url_for(f'categories_bp.categories_{task}', activity=activity, place_id=self.place_id,
                                  destination_id=self.destination_id,
                                  thing_id=self.thing_id, specification_id=self.specification_id)

    def category_url_maker(self, category, task, activity=None):
        if task in ['add', 'remove']:
            return self.refinement_url_maker(category, task, activity=activity)
        else:
            return self.valid_url_for(f'category_bp.category_{task}', category_id=category.id, activity=activity,
                                      destination_id=self.destination_id,
                                      place_id=self.place_id, thing_id=self.thing_id,
                                      specification_id=self.specification_id)

    def choice_url_maker(self, choice, task, activity=None):
        return self.valid_url_for(f'choice_bp.choice_{task}', choice_id=choice.id, activity=activity,
                                  place_id=self.place_id,
                                  destination_id=self.destination_id,
                                  thing_id=self.thing_id, specification_id=self.specification_id)

    def roots_url_maker(self, target, task, activity=None):
        if activity == 'role' and task == 'view':
            return self.role_url_maker(role=self.role, task=task, place_id=0, person_id=self.person_id,
                                       activity=activity)
        else:
            return self.default_url_maker(target, task)

    def role_url_maker(self, role, task, role_id=None, place_id=None, person_id=None, activity=None):
        if place_id is None:
            place_id = self.place_id or 0
        if person_id is None:
            person_id = self.person_id or 0
        if role and isinstance(role, Role):
            role_id = role.id
        else:
            role_id = role_id or 0
        return self.valid_url_for(f'role_bp.role_{task}', role_id=role_id,
                                  place_id=place_id,
                                  person_id=person_id)

    def place_url_maker(self, place, task, activity=None):
        if task == 'view':
            if activity == 'role':
                return self.role_url_maker(self.role, task, place_id=place.id, activity=activity)
            else:
                return self.root_url_maker(place.root, task, place_id=place.id, activity=activity)
        return self.valid_url_for(f'place_bp.place_{task}', activity=activity, place_id=place.id,
                                  thing_id=self.thing_id,
                                  destination_id=self.destination_id,
                                  specification_id=self.specification_id)

    def destination_url_maker(self, destination, task, activity=None):
        return self.root_url_maker(destination.root, 'view', destination_id=destination.id, activity=activity)

    def refinement_url_maker(self, category, task, activity=None):
        return self.valid_url_for(f'refinement_bp.refinement_{task}', category_id=category.id, activity=activity,
                                  destination_id=self.destination_id,
                                  place_id=self.place_id, thing_id=self.thing_id,
                                  specification_id=self.specification_id)

    def root_url_maker(self, root, task, place_id=None, thing_id=None, specification_id=None, activity=None,
                       destination_id=None):
        place_id = place_id or self.place_id or root.place.id
        destination_id = destination_id or self.destination_id or root.place.id
        thing_id = thing_id or self.thing_id or root.thing.id
        specification_id = specification_id or self.specification_id or root.generic_specification.id
        if task == 'view' and activity:
            if activity == 'role':
                place_id = root.place_id
                return self.role_url_maker(self.role, task, place_id=place_id, activity=activity,
                                           person_id=self.person_id)
            else:
                task = f'{task}_{activity}'
                return self.valid_url_for(f'root_bp.root_{task}', place_id=place_id, thing_id=thing_id,
                                          destination_id=destination_id,
                                          specification_id=specification_id)
        else:
            return self.valid_url_for(f'root_bp.root_{task}', activity=activity, place_id=place_id, thing_id=thing_id,
                                      destination_id=destination_id,
                                      specification_id=specification_id)

    def thing_specification_url_maker(self, thing_specification, task, activity=None):
        return self.valid_url_for(f'inventory_bp.inventory_{task}', activity=activity, **thing_specification.identities)

    def user_url_maker(self, user, task, activity=None):
        if activity == 'role':
            if task == 'view':
                person_id = user.id if isinstance(user, User) else 0
                return self.role_url_maker(self.role, task, activity=activity, person_id=person_id)
            elif task == 'list':
                return self.role_url_maker(self.role, task, activity=activity, person_id=0)
        return self.valid_url_for(f'people_bp.people_{task}', activity=activity, person_id=user.id)

    def specification_url_maker(self, category_specification, task, activity=None):
        # No matter the presumed task, do an update
        return self.valid_url_for(f'specification_bp.specification_update',
                                  category_id=category_specification.category.id,
                                  activity=activity, place_id=self.place_id, thing_id=self.thing_id,
                                  destination_id=self.destination_id,
                                  specification_id=self.specification_id)

    def thing_url_maker(self, thing, task, activity=None):
        if task == 'view':
            return self.root_url_maker(thing.root, task, thing_id=thing.id, activity=activity)
        return self.valid_url_for(f'thing_bp.thing_{task}', activity=activity, place_id=self.place_id,
                                  thing_id=self.thing_id,
                                  destination_id=self.destination_id,
                                  specification_id=self.specification_id)

    def target_url(self, target, task, activity=None):
        activity = activity or self.activity or DEFAULT_ACTIVITY
        return self.translator.get(navigational_mark(target), self.default_url_maker)(target, task, activity=activity)

    def valid_url_for(self, endpoint, **kwargs):
        return self.viewer_has_endpoint_role(endpoint) and url_for(endpoint, **kwargs)

    def endpoint_role_names(self, endpoint):
        return self.navigator.endpoint_role_names(endpoint)

    @property
    def is_valid(self):
        return self.root and self.thing and self.place and self.specification and self.destination \
               and self.thing.root == self.root and self.place.root == self.root \
               and self.specification.root == self.root and self.destination.root == self.root

    def may_be_observed(self, viewer):
        return self.is_valid and self.root.may_be_observed(viewer)

    @property
    def thing_specification(self):
        return ThingSpecificationViewer(self.place, self.destination, self.thing, self.specification, self.activity)

    @property
    def current_quantity(self):
        return current_quantity(self.place, self.thing, self.specification)

    @property
    def categories(self):
        return CategoriesViewer(place=self.place, thing=self.thing, specification=self.specification)

    def viewer_has_endpoint_role(self, endpoint):
        roles_to_check = self.navigator.endpoint_role_names(endpoint)
        return self.viewer and any(self.viewer_has_role(role_name) for role_name in roles_to_check)

    @property
    def viewer_is_linked(self):
        return self.root and self.viewer and self.viewer.is_linked(self.root)

    def viewer_has_role(self, required_role_name):
        return required_role_name in self.viewer_role_name_set

    def _viewer_has_role(self, required_role_name):
        if required_role_name in Role.universal_role_name_set:
            return self.viewer.has_universal_role(required_role_name)
        elif required_role_name in Role.root_role_name_set:
            return self.viewer_is_linked and self.root.has_role(self.viewer, required_role_name)
        elif required_role_name in Role.place_role_name_list:
            return self.place and self.viewer_is_linked and self.place.has_role(self.viewer, required_role_name)
        elif required_role_name == Role.super_role_name:
            return self.viewer.is_the_super_admin
        elif required_role_name == Role.self_role_name:
            return self.person and self.person == self.viewer
        elif required_role_name == Role.people_viewer_name:
            return self.viewer.is_the_super_admin or len(self.viewer.linkages) > 0
        elif required_role_name == Role.roots_observer_role_name:
            return self.viewer.is_the_super_admin or len(self.viewer.linkages) > 0
        elif required_role_name == Role.control_role_name:
            if self.role and self.person:
                target_role_name = self.role.name
                granting_role_names = Role.granting_powers.get(target_role_name, [])
                return any(self._viewer_has_role(granting_role_name) for granting_role_name in granting_role_names)
            return False
        elif required_role_name == Role.anybody_role_name:
            return True
        raise ValueError("No such role")


class PlatterById(Platter):
    def __init__(self, viewer=None, activity=DEFAULT_ACTIVITY, root_id=None, place_id=None, thing_id=None,
                 specification_id=None, destination_id=None, person_id=None, role_id=None):
        role = role_id and find_role_by_id(role_id)
        root = root_id and find_root_by_id(root_id)
        place = place_id and find_place_by_id(place_id)
        person = person_id and find_person_by_id(person_id)
        destination = destination_id and Destination(find_place_by_id(destination_id))
        thing = thing_id and find_thing_by_id(thing_id)
        specification = specification_id and find_specification_by_id(specification_id)
        Platter.__init__(self, viewer=viewer, activity=activity, root=root, place=place, thing=thing,
                         specification=specification, destination=destination, person=person, role=role)
