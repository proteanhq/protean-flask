""" Serializers used by the sample app """
from protean_flask.core.serializers import EntitySerializer
from protean_flask.core.serializers import ma

from .entities import Dog
from .entities import Human
from .entities import RelatedDog


class DogSerializer(EntitySerializer):
    """ Serializer for Dog Entity"""

    class Meta:
        entity = Dog


class HumanSerializer(EntitySerializer):
    """ Serializer for Human Entity"""

    class Meta:
        entity = Human


class HumanDetailSerializer(EntitySerializer):
    """ Serializer for the Human Entity with association"""
    dogs = ma.fields.Nested('RelatedDogSerializer', many=True,
                            exclude=['owner'])

    class Meta:
        entity = Human


class RelatedDogSerializer(EntitySerializer):
    """ Serializer for the Related Dpg Entity"""
    owner = ma.fields.Nested(HumanSerializer)

    class Meta:
        entity = RelatedDog
