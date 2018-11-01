""" Schemas used by the sample app"""
from protean.core.repository import repo_factory
from protean.impl.repository.dict_repo import DictSchema

from .entities import Dog


class DogSchema(DictSchema):
    """ Schema for the Dog Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Dog
        schema_name = 'dogs'


repo_factory.register(DogSchema)
