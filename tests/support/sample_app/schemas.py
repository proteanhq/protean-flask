""" Schemas used by the sample app"""
from protean.core.repository import repo_factory
from protean.impl.repository.dict_repo import DictModel

from .entities import Dog
from .entities import Human


class DogModel(DictModel):
    """ Schema for the Dog Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Dog
        schema_name = 'dogs'


class HumanModel(DictModel):
    """ Schema for the Human Entity Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Human
        schema_name = 'humans'


repo_factory.register(DogModel)
repo_factory.register(HumanModel)
