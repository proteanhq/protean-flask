"""This module holds the generic definitions of Seralizer"""

from datetime import datetime

import pytz
from flask_jwt_extended import get_jwt_identity
from flask_marshmallow import Marshmallow
from marshmallow import fields

MARSHMALLOW = Marshmallow()


class BaseSchema(MARSHMALLOW.Schema):
    """Base Marshmallow Schema for all serializers"""

    message = fields.Dict(values=fields.String(), keys=fields.String())
    type = fields.String()


class UserTimezone(fields.Field):
    """Class to format timestamp in user's timezone"""

    def _serialize(self, value, attr, obj):
        user_timezone = 'Australia/Melbourne'
        if get_jwt_identity() and get_jwt_identity()['timezone']:
            user_timezone = get_jwt_identity()['timezone']
        return self._timezone_conversion(value, user_timezone)

    def _timezone_conversion(self, value, user_timezone):
        """
        :param value:
        :param user_timezone:
        :return: ast timezone
        """
        utc = pytz.timezone('UTC')
        if not isinstance(value, str):
            value = value.isoformat('T')
        created = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        result = utc.localize(created, is_dst=None).astimezone(pytz.utc)
        return result.astimezone(pytz.timezone(
            user_timezone)).strftime("%Y-%m-%dT%H:%M:%S")


class DictToArray(fields.Field):
    """convert dict of dicts to an array and serialize"""

    def __init__(self, nested_field, *args, **kwargs):
        fields.Field.__init__(self, *args, **kwargs)
        self.nested_field = nested_field

    def _serialize(self, value, attr, obj):
        array = []
        for key in value.keys():
            array.append(self.nested_field.serialize(
                key, self.get_value(attr, obj)))
        return array
