""" Views of the sample app"""
from protean_flask.core.view import ShowAPIResource

from .serializers import DogSerializer
from .schemas import DogSchema


class ShowDogResource(ShowAPIResource):
    """ View for retrieving a Dog by its ID"""
    schema_cls = DogSchema
    serializer_cls = DogSerializer
