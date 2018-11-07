""" Views of the sample app"""
from protean_flask.core.views import (ShowAPIResource, ListAPIResource,
                                      CreateAPIResource, UpdateAPIResource,
                                      DeleteAPIResource)
from protean_flask.core.viewsets import GenericAPIResourceSet

from .serializers import DogSerializer, HumanSerializer
from .schemas import DogSchema, HumanSchema
from .usecases import ListMyDogsUsecase, ListMyDogsRequestObject


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


class HumanResourceSet(GenericAPIResourceSet):
    """ Resource Set for the Human Entity"""
    schema_cls = HumanSchema
    serializer_cls = HumanSerializer

    def my_dogs(self, identifier):
        """ List all the dogs belonging to the Human"""
        # Run the usecase and get the related dogs
        payload = {'identifier': identifier}
        response_object = self._process_request(
            ListMyDogsUsecase, ListMyDogsRequestObject, payload=payload,
            no_serialization=True)

        # Serialize the results and return the response
        serializer = DogSerializer(many=True)
        items = serializer.dump(response_object.value.items)
        result = {
            'dogs': items.data,
            'total': response_object.value.total,
            'page': response_object.value.page
        }
        return result, response_object.code.value


def flask_view():
    """ A non protean flask view """
    return 'View Response', 200
