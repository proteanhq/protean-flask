"""Module that defines entry point to the Protean Flask Application"""
from flask import Request, request, current_app

from protean.core.exceptions import UsecaseExecutionError
from protean.utils.importlib import perform_import
from protean.conf import active_config

from .views import APIResource


class ProteanRequest(Request):
    """ Custom request object to store protean specific code"""
    payload = None


class Protean(object):
    """
    The main entry point for the application.
    You need to initialize it with a Flask Application.

    >>> app = Flask(__name__)
    >>> api = Protean(app)

    Alternatively, you can use :meth:`init_app` to set the Flask application
    after it has been constructed.

    :param app: the Flask application object
    :type app: flask.Flask or flask.Blueprint

    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
        self.app = app

    def init_app(self, app):
        """Perform initialization actions with the given :class:`flask.Flask`
        object.

        :param app: The flask application object
        :type app: flask.Flask
        """
        # Update the request class for the app
        app.request_class = ProteanRequest

        # Register error handlers for the app
        app.register_error_handler(UsecaseExecutionError,
                                   self._handle_exception)
        # Set the default configurations
        app.config.setdefault('DEFAULT_RENDERER',
                              'protean_flask.core.renderers.render_json')
        app.config.setdefault('DEFAULT_CONTENT_TYPE', 'application/json')
        app.config.setdefault('EXCEPTION_HANDLER', None)

        # Update the current configuration
        app.config.from_object(active_config)

    def register_viewset(self, view, endpoint, url, module, resource,
                         p_key='identifier', pk_type='string',
                         additional_routes=None):
        """Register a Viewset

        Pass the Resource class along with the URL
            `module` should be the folder that contains views.py, entities.py etc.
            `resource` is the name around which all other classes will be derived

        Additional routes (apart from the standard five) can be specified via
            `additional_routes` argument. Note that the route names have to be
            the same as method names
        """
        if additional_routes is None:
            additional_routes = list()
        view_func = view.as_view(endpoint, module=module, resource=resource)

        # Custom Routes
        for route in additional_routes:
            self.app.add_url_rule(
                '{}{}'.format(url, route), view_func=view_func)

        # Standard routes
        self.app.add_url_rule(url, defaults={p_key: None},
                              view_func=view_func, methods=['GET', ])
        self.app.add_url_rule(url, view_func=view_func, methods=['POST', ])
        self.app.add_url_rule('%s<%s:%s>' % (url, pk_type, p_key),
                              view_func=view_func,
                              methods=['GET', 'PUT', 'DELETE'])

    def _handle_exception(self, e):
        """ Handle Protean exceptions and return appropriate response """

        # Get the renderer from the view class
        renderer = perform_import(current_app.config['DEFAULT_RENDERER'])
        if request.url_rule:
            view_func = current_app.view_functions[request.url_rule.endpoint]
            view_class = view_func.view_class
            if isinstance(view_func, APIResource):
                renderer = view_class.get_renderer()

        # Default to Server Error
        default_message = {
            'code': 500, 'message': "Something went wrong. Please try later!!"}
        code, data, headers = 500, default_message, {}

        # If user has defined an exception handler then call that
        exception_handler = perform_import(
            current_app.config['EXCEPTION_HANDLER'])
        if exception_handler:
            code, data, headers = exception_handler(e)

        elif isinstance(e, UsecaseExecutionError):
            code = e.value[0].value
            data = e.value[1]

        # Build the response and return it
        response = renderer(data, code, headers)
        return response
