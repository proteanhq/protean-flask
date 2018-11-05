""" Serializers used by the sample app """
from marshmallow import fields

from protean_flask.core.serializers import EntitySerializer

from .entities import Dog


class DogSerializer(EntitySerializer):
    """ Serializer for Dog Entity"""

    class Meta:
        entity = Dog
