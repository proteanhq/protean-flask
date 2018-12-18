""" Serializers used by the sample app """
from protean_flask.core.serializers import EntitySerializer

from .entities import Dog
from .entities import Human


class DogSerializer(EntitySerializer):
    """ Serializer for Dog Entity"""

    class Meta:
        entity = Dog


class HumanSerializer(EntitySerializer):
    """ Serializer for Human Entity"""

    class Meta:
        entity = Human
