""" Usecases of the sample application """

from protean.core.tasklet import Tasklet
from protean.core.usecase import ListRequestObject
from protean.core.usecase import ListUseCase
from protean.core.usecase import ShowRequestObject
from protean.core.usecase import UseCase

from .schemas import DogSchema
from .schemas import repo


class ListMyDogsRequestObject(ShowRequestObject):
    """ Request object for the my dogs use case """


class ListMyDogsUsecase(UseCase):
    """ Use case for listing dogs of a human """
    def process_request(self, request_object):
        """ Get the human and return the dogs owned by the human"""
        human = self.repo.get(request_object.identifier)

        # Get the dogs related to the human
        payload = {'owner': human.name, 'order_by': ['age']}
        response_object = Tasklet.perform(
            repo, DogSchema, ListUseCase, ListRequestObject, payload,
            raise_error=True)
        return response_object
