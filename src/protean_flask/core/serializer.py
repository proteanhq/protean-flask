"""This module holds the generic definitions of Seralizer"""

from marshmallow import fields, Schema


class BaseSchema(Schema):
    """Base Marshmallow Schema for all serializers"""


class DictToArray(fields.Field):
    """convert dict of dicts to an array and serialize"""

    def __init__(self, nested_field, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.nested_field = nested_field

    def _serialize(self, value, attr, obj):
        array = []
        for key in value.keys():
            array.append(self.nested_field.serialize(
                key, self.get_value(attr, obj)))
        return array
