"""This module exposes the Base Resource View for all Application Views"""

import importlib

import inflect
import inflection

from flask import request, current_app
from flask.views import MethodView

from protean.core.usecase import ShowRequestObject, ShowUseCase
from protean.core.tasklet import Tasklet
from protean.core.transport import ResponseFailure
from protean.core.repository import repo_factory

from protean_flask.core.renderers import render_json

INFLECTOR = inflect.engine()


class APIResource(MethodView):
    """The base resource view that allows defining custom methods other than
    the standard five REST routes. Also handles rendering the output to json.

    """
    renderer = render_json

    def dispatch_request(self, *args, **kwargs):
        """Dispatch the request to the correct function"""

        # Lookup custom method defined for this resource
        func = request.url_rule.rule.rsplit('/', 1)[-1]
        if func and (func[0] != '<' and func[1] != '>'):
            meth = getattr(self, func, None)
        else:
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
            response = APIResource.renderer(data, code, headers)

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
        Defaults to using `self.entity_class`.
        """
        assert self.schema_cls is not None, (
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
        assert self.serializer_cls is not None, (
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
            rf, schema_cls, usecase_cls, request_object_cls,payload)

        if isinstance(response_object, ResponseFailure):
            print(vars(response_object))
            return response_object.value, response_object.code

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


class GenericAPIResourceSet(GenericAPIResource):
    """This is the Generic Base Class for all Views

       It also serves as a template where a resource requires no customisations,
       and wants to offer just CRUD operations
    """
    serializer_class = None
    repo_factory = None

    def __init__(self, module, resource, repository_factory):
        """Initialize Generic API and register routes"""

        # The module where classes related to this resource
        # can be found. For example, if `synonym` resource was defined
        # in 'src/taxonomy/views.py', then the module should be 'taxonomy'.
        # It is the folder in which all other files (views.py, entities.py,
        # serializers.py, usecases.py etc) will be found.
        self.module = module

        # 'resource' is used to derive other associated classes. For example,
        # if resource is 'synonym', then the serializer class will be
        # `SynonymSerializer`, the List UseCase class will be `ListSynonymUseCase`,
        # the entity will be `Synonym` and so on.
        self.resource = resource

        # 'repository_factory` provides access to defined repositories
        self.repository_factory = repository_factory

        # Pluralize the resource string
        self.url = '/{}/'.format(INFLECTOR.plural(self.resource))

        # Method Aliases to take advantage of MethodView type routing
        self.post = self.create
        self.put = self.update

    def _derive_module(self, resource_type):
        """Derive views module from module base"""
        module = None
        if resource_type == 'view':
            module = importlib.import_module('{}.views'.format(self.module))
        elif resource_type == 'serializer':
            module = importlib.import_module('{}.serializers'.format(self.module))
        elif resource_type == 'usecase' or resource_type == 'request_object':
            module = importlib.import_module('{}.usecases'.format(self.module))
        elif resource_type == 'entity':
            module = importlib.import_module('{}.entities'.format(self.module))
        return module

    def _get_class(self, resource_type, class_name):
        """Get class from module and class name strings"""
        module = self._derive_module(resource_type)
        class_ = getattr(module, class_name)
        return class_

    def _get_class_instance(self, resource_type, class_name, *args, **kwargs):
        """Construct and return an instance from module and class name strings"""
        class_ = self._get_class(resource_type, class_name)
        return class_(*args, **kwargs)

    def _derive_entity_cls(self):
        """Derive the connected Entity class"""
        return self.resource.title()

    def _derive_resource_cls(self):
        """Derive the connected Entity class"""
        return '{}Resource'.format(self.resource.title())

    def _derive_serializer_cls(self, many=False):
        """Derive the appropriate serializer class from type of response"""
        if many:
            class_ = '{}BriefSerializer'.format(self.resource.title())
        else:
            class_ = '{}Serializer'.format(self.resource.title())

        return class_

    def _derive_usecase_cls(self, method):
        """Derive the appropriate UseCase class from type of response"""

        return {
            'index': 'List{}UseCase'.format(INFLECTOR.plural(self.resource.title())),
            'show': 'Show{}UseCase'.format(self.resource.title()),
            'create': 'Create{}UseCase'.format(self.resource.title()),
            'update': 'Update{}UseCase'.format(self.resource.title()),
            'delete': 'Delete{}UseCase'.format(self.resource.title())
        }.get(method, None)

    def _derive_request_object_cls(self, method):
        """Derive the appropriate UseCase class from type of response"""

        return {
            'index': 'List{}RequestObject'.format(INFLECTOR.plural(self.resource.title())),
            'show': 'Show{}RequestObject'.format(self.resource.title()),
            'create': 'Create{}RequestObject'.format(self.resource.title()),
            'update': 'Update{}RequestObject'.format(self.resource.title()),
            'delete': 'Delete{}RequestObject'.format(self.resource.title())
        }.get(method, None)
