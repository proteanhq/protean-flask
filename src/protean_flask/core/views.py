"""This module exposes the Base Resource View for all Application Views"""

import json

import inflect
import inflection

from flask import request, current_app
from flask.views import MethodView

from protean.core.usecase import (ShowRequestObject, ShowUseCase,
                                  ListRequestObject, ListUseCase,
                                  CreateRequestObject, CreateUseCase,
                                  UpdateRequestObject, UpdateUseCase,
                                  DeleteRequestObject, DeleteUseCase)
from protean.core.tasklet import Tasklet
from protean.core.transport import ResponseFailure
from protean.core.repository import repo_factory
from protean.utils import perform_import

INFLECTOR = inflect.engine()


class APIResource(MethodView):
    """The base resource view that allows defining custom methods other than
    the standard five REST routes. Also handles rendering the output to json.

    """

    def get_renderer(self):
        """ Return the renderer to be used for this resource """
        # If the view does not define a renderer then return the default
        renderer = getattr(self, 'renderer', None)
        if not renderer:
            renderer = perform_import(
                current_app.config['DEFAULT_RENDERER'])

        return renderer

    def dispatch_request(self, *args, **kwargs):
        """Dispatch the request to the correct function"""

        # Lookup custom method defined for this resource
        func = request.url_rule.rule.rsplit('/', 1)[-1]
        meth = None
        if func and (func[0] != '<' and func[1] != '>'):
            meth = getattr(self, func, None)

        if not meth:
            meth = getattr(self, request.method.lower(), None)

        # If the request method is HEAD and we don't have a handler for it
        # retry with GET.
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)

        assert meth is not None, 'Unimplemented method %r' % request.method

        # Call the method and create the response
        response = meth(*args, **kwargs)
        if not isinstance(response, current_app.response_class):
            data, code, headers = self._unpack_response(response)
            response = self.get_renderer()(data, code, headers)

        return response

    @staticmethod
    def _unpack_response(value):
        """Return a three tuple of data, code, and headers"""
        if not isinstance(value, tuple):
            return value, 200, {}

        try:
            data, code, headers = value
            return data, code, headers
        except ValueError:
            pass

        try:
            data, code = value
            return data, code, {}
        except ValueError:
            pass

        return value, 200, {}


class GenericAPIResource(APIResource):
    """This is the Generic Base Class for all Views
    """

    schema_cls = None
    serializer_cls = None
    repo_factory = None

    def get_repository_factory(self):
        """ Returns the repository factory to be used
        Uses the attribute `self.repo_factory` or
        defaults to using `protean.repository.rf`.
        """
        return self.repo_factory or repo_factory

    def get_schema_cls(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.schema_cls`.
        """
        if not self.schema_cls:
            raise AssertionError(
                "'%s' should either include a `schema_cls` attribute, "
                "or override the `get_schema_cls()` method."
                % self.__class__.__name__
            )
        return self.schema_cls

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        de-serializing input, and for serializing output.
        """
        serializer_cls = self.get_serializer_cls()
        serializer = serializer_cls(*args, **kwargs)
        serializer.context = self.get_serializer_context()
        return serializer

    def get_serializer_cls(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        """
        if not self.serializer_cls:
            raise AssertionError(
                "'%s' should either include a `serializer_cls` attribute, "
                "or override the `get_serializer_cls()` method."
                % self.__class__.__name__
            )
        return self.serializer_cls

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'view': self
        }

    def _process_request(self, usecase_cls, request_object_cls, payload,
                         many=False, no_serialization=False):

        # Get the resource name
        schema_cls = self.get_schema_cls()
        resource = inflection.underscore(schema_cls.opts.entity_cls.__name__)

        # Get the serializer for this class
        serializer = None
        if not no_serialization:
            serializer = self.get_serializer(many=many)

        # Get the repository factory to be used
        rf = self.get_repository_factory()

        # Run the use case and return the results
        response_object = Tasklet.perform(
            rf, schema_cls, usecase_cls, request_object_cls, payload)

        if isinstance(response_object, ResponseFailure):
            return response_object.value, response_object.code.value

        elif many:
            items = serializer.dump(response_object.value.items)
            result = {
                INFLECTOR.plural(resource): items.data,
                'total': response_object.value.total,
                'page': response_object.value.page
            }
            return result, response_object.code.value

        else:
            result = serializer.dump(response_object.value)
            return {resource: result.data}, response_object.code.value


class ShowAPIResource(GenericAPIResource):
    """ An API view for retrieving an entity by its identifier"""

    usecase_cls = ShowUseCase
    request_object_cls = ShowRequestObject

    def get(self, identifier):
        """Show the entity.
        Expected Parameters:
             identifier = <string>, identifies the entity
        """
        payload = {'identifier': identifier}
        return self._process_request(
            self.usecase_cls, self.request_object_cls, payload=payload)


class ListAPIResource(GenericAPIResource):
    """ An API view for listing entities"""

    usecase_cls = ListUseCase
    request_object_cls = ListRequestObject

    def get(self):
        """List the entities.
        """
        # Convert immutable dict to dict
        payload = request.args.to_dict(flat=False)

        # Remove trailing [] for list attrs
        for key in payload:
            val = payload.pop(key)
            if len(val) > 1 or key.endswith('[]'):
                payload[key.strip('[]')] = val
            else:
                payload[key] = val[0]

        return self._process_request(
            self.usecase_cls, self.request_object_cls, payload=payload,
            many=True)


class CreateAPIResource(GenericAPIResource):
    """ An API view for creating an entity"""

    usecase_cls = CreateUseCase
    request_object_cls = CreateRequestObject

    def post(self):
        """Create the entity.
        """
        payload = json.loads(request.data)
        return self._process_request(
            self.usecase_cls, self.request_object_cls, payload=payload)


class UpdateAPIResource(GenericAPIResource):
    """ An API view for updating an entity"""

    usecase_cls = UpdateUseCase
    request_object_cls = UpdateRequestObject

    def put(self, identifier):
        """Update the entity.
         Expected Parameters:
             identifier = <string>, identifies the entity
        """
        payload = json.loads(request.data)
        payload.update({'identifier': identifier})
        return self._process_request(
            self.usecase_cls, self.request_object_cls, payload=payload)


class DeleteAPIResource(GenericAPIResource):
    """ An API view for deleting an entity"""

    usecase_cls = DeleteUseCase
    request_object_cls = DeleteRequestObject

    def delete(self, identifier):
        """Delete the entity.
         Expected Parameters:
             identifier = <string>, identifies the entity
        """
        payload = {'identifier': identifier}
        return self._process_request(
            self.usecase_cls, self.request_object_cls, payload=payload)
