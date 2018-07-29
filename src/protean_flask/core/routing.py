"""Module that defines utility functions for Flask Routing"""


def register_api(app, view, endpoint,
                 url, module, resource,
                 p_key='identifier',
                 pk_type='string',
                 additional_routes=None):
    """Register Classes/Views/Routes

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
        app.add_url_rule('{}{}'.format(url, route), view_func=view_func)

    # Standard routes
    app.add_url_rule(url, defaults={p_key: None},
                     view_func=view_func, methods=['GET', ])
    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, p_key), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])
