""" Views of the sample app"""
from protean.context import context

from protean_flask.core.views import APIResource
from protean_flask.core.views import CreateAPIResource
from protean_flask.core.views import DeleteAPIResource
from protean_flask.core.views import ListAPIResource
from protean_flask.core.views import ShowAPIResource
from protean_flask.core.views import UpdateAPIResource
from protean_flask.core.viewsets import GenericAPIResourceSet

from .entities import Dog
from .entities import Human
from .serializers import DogSerializer
from .serializers import HumanSerializer
from .usecases import ListMyDogsRequestObject
from .usecases import ListMyDogsUsecase


class ShowDogResource(ShowAPIResource):
    """ View for retrieving a Dog by its ID"""
    entity_cls = Dog
    serializer_cls = DogSerializer


class ListDogResource(ListAPIResource):
    """ View for listing Dog entities"""
    entity_cls = Dog
    serializer_cls = DogSerializer


class CreateDogResource(CreateAPIResource):
    """ View for creating a Dog Entity"""
    entity_cls = Dog
    serializer_cls = DogSerializer


class UpdateDogResource(UpdateAPIResource):
    """ View for updating a Dog by its ID"""
    entity_cls = Dog
    serializer_cls = DogSerializer


class DeleteDogResource(DeleteAPIResource):
    """ View for deleting a Dog by its ID"""
    entity_cls = Dog
    serializer_cls = DogSerializer


class HumanResourceSet(GenericAPIResourceSet):
    """ Resource Set for the Human Entity"""
    entity_cls = Human
    serializer_cls = HumanSerializer

    def my_dogs(self, identifier):
        """ List all the dogs belonging to the Human"""
        # Run the usecase and get the related dogs
        payload = {'identifier': identifier}
        dogs_list = self._process_request(
            ListMyDogsUsecase, ListMyDogsRequestObject, payload=payload,
            no_serialization=True)

        # Serialize the results and return the response
        serializer = DogSerializer(many=True)
        items = serializer.dump(dogs_list.items)
        page = int(dogs_list.offset / dogs_list.limit) + 1
        result = {
            'dogs': items.data,
            'total': dogs_list.total,
            'page': page
        }
        return result, 200


def flask_view():
    """ A non protean flask view """
    return 'View Response', 200


class CurrentContextResource(APIResource):
    """ View for retrieving the current context information """

    def get(self):
        """ Return the context information on GET """
        context_data = {
            'host_url': context.host_url,
            'url': context.url,
            'tenant_id': context.tenant_id,
            'user_agent': context.user_agent,
            'user_agent_hash': context.user_agent_hash,
            'remote_addr': context.remote_addr
        }
        return context_data
