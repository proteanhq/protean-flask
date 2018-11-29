""" Entities used by the sample application """
from protean.core.entity import Entity
from protean.core import field


class Dog(Entity):
    """This is a dummy Dog Entity class"""
    id = field.Integer(identifier=True)
    name = field.String(required=True, max_length=50)
    age = field.Integer(default=5)
    owner = field.String(required=True, max_length=15)


class Human(Entity):
    """ This is a dummy Human class """
    id = field.Integer(identifier=True)
    name = field.String(required=True, max_length=50)
    contact = field.StringMedium()
