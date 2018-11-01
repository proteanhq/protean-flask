""" Serializers used by the sample app """
from protean_flask.core.serializer import BaseSchema

from marshmallow import fields


class DogSerializer(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    age = fields.Integer()
    owner = fields.String()
