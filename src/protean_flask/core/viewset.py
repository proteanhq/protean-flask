"""This module exposes a generic Viewset class"""
import importlib

from protean_flask.core.view import GenericAPIResource, INFLECTOR


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
