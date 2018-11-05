""" Views of the sample app"""
from protean_flask.core.views import (ShowAPIResource, ListAPIResource,
                                      CreateAPIResource, UpdateAPIResource,
                                      DeleteAPIResource)

from .serializers import DogSerializer
from .schemas import DogSchema


class ShowDogResource(ShowAPIResource):
    """ View for retrieving a Dog by its ID"""
    schema_cls = DogSchema
    serializer_cls = DogSerializer


class ListDogResource(ListAPIResource):
    """ View for listing Dog entities"""
    schema_cls = DogSchema
    serializer_cls = DogSerializer


class CreateDogResource(CreateAPIResource):
    """ View for creating a Dog Entity"""
    schema_cls = DogSchema
    serializer_cls = DogSerializer


class UpdateDogResource(UpdateAPIResource):
    """ View for updating a Dog by its ID"""
    schema_cls = DogSchema
    serializer_cls = DogSerializer


class DeleteDogResource(DeleteAPIResource):
    """ View for deleting a Dog by its ID"""
    schema_cls = DogSchema
    serializer_cls = DogSerializer
