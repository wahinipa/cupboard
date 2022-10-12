#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for

from tracking import database
from tracking.cardistry.models.cardistry_models import name_is_key
from tracking.commons.cupboard_display_context import CupboardDisplayContextMixin, CupboardDisplayContext
from tracking.modelling.base_models import UniqueNamedBaseModel


class Root(CupboardDisplayContextMixin, UniqueNamedBaseModel):
    singular_label = "Root"
    plural_label = "Roots"

    place_id = database.Column(database.Integer, database.ForeignKey('place.id'), unique=True, nullable=False)
    thing_id = database.Column(database.Integer, database.ForeignKey('thing.id'), unique=True, nullable=False)

    @property
    def classification(self):
        return 'Organizational Association'

    @property
    def delete_url(self):
        return url_for('root_bp.root_delete', root_id=self.id)

    @property
    def update_url(self):
        return url_for('root_bp.root_update', root_id=self.id)

    def may_be_observed(self, viewer):
        return True

    def may_delete(self, viewer):
        return viewer.may_delete_root

    def may_update(self, viewer):
        return viewer.may_update_root

    @property
    def parent_object(self):
        return None

    @property
    def page_template(self):
        return "pages/root_view.j2"

    @property
    def url(self):
        return url_for('root_bp.root_view', root_id=self.id)

    def viewable_children(self, viewer):
        return [self.place, self.thing]


def all_roots():
    return sorted(Root.query.all(), key=name_is_key)


def all_root_display_context(viewer):
    context = root_display_context(viewer, "pages/home_page.j2")
    for root in all_roots():
        context.add_child_display_context(root.display_context(viewer))
    if viewer.may_create_root:
        context.add_task(url=url_for('root_bp.root_create'), label="Root", task="create")
    return context


def root_display_context(viewer, page_template='pages/form_page.j2'):
    context = CupboardDisplayContext(page_template=page_template)
    context.add_attribute('label', 'Home')
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
