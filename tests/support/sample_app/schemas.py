""" Schemas used by the sample app"""
from protean.core.repository import repo_factory
from protean.impl.repository.dict_repo import DictModel

from .entities import Dog
from .entities import Human
from .entities import RelatedDog


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


class RelatedDogModel(DictModel):
    """ Schema for the RelatedDog Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = RelatedDog
        schema_name = 'related_dogs'


repo_factory.register(DogModel)
repo_factory.register(HumanModel)
repo_factory.register(RelatedDogModel)
