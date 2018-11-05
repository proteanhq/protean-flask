""" Serializers used by the sample app """
from marshmallow import fields

from protean_flask.core.serializers import BaseSchema


class DogSerializer(BaseSchema):
    """ Serializer for Dog Entity"""
    id = fields.Integer()
    name = fields.String()
    age = fields.Integer()
    owner = fields.String()
