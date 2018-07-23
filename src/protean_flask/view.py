"""This module exposes the Base Resource View for all Application Views"""

import json
import importlib
import inflect

from flask.views import View, MethodViewType
from flask._compat import with_metaclass
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.view_decorators import verify_jwt_in_request

from protean.transport import Status

INFLECTOR = inflect.engine()


class CustomMethodView(with_metaclass(MethodViewType, View)):
    """A very simplistic implementation of routing to methods other than
    the standard five REST routes. This needs a better implementation, probably
    decorator based wrapping, to work in all scenarios

    We need to create a parallel implementation of MethodView because
    MethodView by default only looks at request methods (GET, POST, PUT and DELETE)
    and automatically routes a request to the appropriate method. There is no
    support for defining custom routes
    """

    # fixme handle this functionality more elegantly
    # Refer to Blueprint.register for clues

    def dispatch_request(self, *args, **kwargs):
        """Dispatch the request to the correct function"""
        function = request.url_rule.rule.rsplit('/', 1)[-1]
        if function and (function[0] != '<' and function[1] != '>'):
            meth = getattr(self, function, None)
        else:
            meth = getattr(self, request.method.lower(), None)

            # If the request method is HEAD and we don't have a handler for it
            # retry with GET.
            if meth is None and request.method == 'HEAD':
                meth = getattr(self, 'get', None)

        assert meth is not None, 'Unimplemented method %r' % request.method
        return meth(*args, **kwargs)


class GenericAPIResource(CustomMethodView):
    """This is the Generic Base Class for all Views

       It also serves as a template where a resource requires no customisations,
       and wants to offer just CRUD operations
    """

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

    def _process_request(self, method, params):
        """Construct necessary classes and execute request

        `method` determines which usecase is to be called
        `params` contains the request args that need to be fed to usecase,
        via the request object.
        """
        use_case = self._get_class_instance('usecase',
                                            self._derive_usecase_cls(method),
                                            self.repository_factory)

        # Derive Entity Class and Request Object class to feed to Usecase
        request_object_cls = self._get_class('request_object',
                                             self._derive_request_object_cls(method))
        entity_cls = self._get_class('entity',
                                     self._derive_entity_cls())
        request_object = request_object_cls.from_dict(entity_cls, params)

        return use_case.execute(request_object)

    def get(self, identifier=None):
        """This is the method connected to `GET` HTTP Verb.

        We will route to either `index` method or `show`, depending on
        the presense of identifier.
        """

        if identifier:
            response = self.show(identifier)
        else:
            response = self.index()

        return response

    def index(self):
        """INDEX method"""

        response_object = self._process_request('index', request.args)

        serializer = self._get_class_instance('serializer',
                                              self._derive_serializer_cls(),
                                              many=True)

        if 'data' in response_object.value:
            result = serializer.dump(response_object.value['data'])

            return (jsonify(
                {INFLECTOR.plural(self.resource): result.data,
                 "total": response_object.value["total"],
                 "page": response_object.value["page"]}),
                    Status(response_object.type))

        return (jsonify({"message": response_object.value}),
                Status(response_object.type))

    def create(self):
        """CREATE method"""

        data_json = json.loads(request.data)
        data_json.update({
            'created_by': get_jwt_identity()['user_id'],
            'updated_by': get_jwt_identity()['user_id'],
            'tenant_id': get_jwt_identity()['tenant_id']
            })

        response_object = self._process_request('create', data_json)
        serializer = self._get_class_instance('serializer', self._derive_serializer_cls())
        if response_object:
            result = serializer.dump(response_object.value)
            return jsonify({self.resource: result.data}), Status.SUCCESS_CREATED

        return (jsonify({"message": response_object.value}),
                Status(response_object.type))

    def update(self, identifier=None):
        """UPDATE method

        Expected Paramters:
            identifier = <int>, default is None
        """

        data_json = json.loads(request.data)
        data_json.update({
            'identifier': identifier,
            'updated_by': get_jwt_identity()['user_id']})

        response_object = self._process_request('update', data_json)

        serializer = self._get_class_instance('serializer', self._derive_serializer_cls())
        result = serializer.dump(response_object.value)
        return jsonify({self.resource: result.data}), Status(response_object.type)

    def show(self, identifier=None):
        """SHOW method

        Expected Paramters:
            identifier = <string>, default is None
        """
        response_object = self._process_request('show', {'identifier': identifier})

        serializer = self._get_class_instance('serializer', self._derive_serializer_cls())
        result = serializer.dump(response_object.value)
        return jsonify({self.resource: result.data}), Status(response_object.type)

    def delete(self, identifier=None):
        """DELETE method

        Expected Paramters:
            identifier = <string>, default is None
        """

        response_object = self._process_request('delete', {'identifier': identifier})

        return (jsonify({'message': response_object.value}),
                Status(response_object.type))


class GenericProtectedAPIResource(GenericAPIResource):
    """This is the base class for authenticated APIs"""

    def authenticated(self):  # pylint: disable=E0213
        """Decorate MethodView for JWT authentication

        Just wrapping with `authenticated` method of flask_jwt did not work
        This link exposed the idea of using `_authenticated` (with a underscore at the front)
        and writing a custom decorator, which is then wrapped over MethodView methods:
        https://github.com/web-pal/flask-rest-boilerplate/blob/master/init/jwt_init.py

        """
        def decorator(*args, **kwargs):
            """Wrap `_authenticated` method of flask_jwt"""
            verify_jwt_in_request()
            return self(*args, **kwargs)  # pylint: disable=E1102
        return decorator

    decorators = [authenticated]
