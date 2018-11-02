"""Module that defines entry point to the Protean Flask Application"""
from protean.conf import active_config


class Protean(object):
    """
    The main entry point for the application.
    You need to initialize it with a Flask Application.
    """

    def __init__(self, app=None):
        if app is not None:
            self.app = app
        self.init_app(app)

    def init_app(self, app):
        """Perform initialization actions with the given :class:`flask.Flask`
        object.

        :param app: The flask application object
        :type app: flask.Flask
        """
        # Set the default configurations
        app.config.setdefault('DEFAULT_RENDERER',
                              'protean_flask.core.renderers.render_json')

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
                              view_func=view_func, methods=['GET', 'PUT', 'DELETE'])
