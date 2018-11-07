""" Schemas used by the sample app"""
from protean.core.repository import repo_factory
from protean.impl.repository.dict_repo import DictSchema

from .entities import Dog, Human


class DogSchema(DictSchema):
    """ Schema for the Dog Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Dog
        schema_name = 'dogs'


class HumanSchema(DictSchema):
    """ Schema for the Human Entity Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Human
        schema_name = 'humans'


repo_factory.register(DogSchema)
repo_factory.register(HumanSchema)
