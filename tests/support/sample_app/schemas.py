""" Schemas used by the sample app"""
from protean.core.repository import repo
from protean.impl.repository.dict_repo import DictSchema

from .entities import Dog
from .entities import Human


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


repo.register(DogSchema)
repo.register(HumanSchema)
