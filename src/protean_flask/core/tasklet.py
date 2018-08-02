"""This module defines utilities to process a UseCase"""

import inflect
import inflection
from flask import jsonify
from protean.core.transport import Status
from protean.core.usecase import Tasklet

INFLECTOR = inflect.engine()


class APITasklet:
    """Utility class to execute UseCases"""

    @classmethod
    def perform(cls, repo_factory, cls_entity, cls_usecase, cls_request_object,
                cls_serializer, payload, many=False, no_serialization=False):
        """This method bundles all essential artifacts and initiates usecase execution"""

        resource = inflection.underscore(cls_entity.__name__)

        # Ensure that serializer class is specified if no_serialization flag is False
        serializer = None
        if cls_serializer is None:
            assert no_serialization is True
        else:
            serializer = cls_serializer(many=many)
            serializer.context = {'repo_factory': repo_factory}

        response_object = Tasklet.perform(repo_factory, cls_entity, cls_usecase,
                                          cls_request_object, payload, many)

        # FIXME Check for Response object value
        if many:
            if no_serialization:
                return response_object.value['data']
            else:
                import pdb; pdb.set_trace()
                result = serializer.dump(response_object.value['data'])
                return jsonify({INFLECTOR.plural(resource): result.data,
                                "total": response_object.value['total'],
                                "page": response_object.value['page']}), \
                    Status(response_object.code).value
        else:
            if no_serialization:
                return response_object.value
            else:
                result = serializer.dump(response_object.value)
                return jsonify({resource: result.data}), Status(response_object.code).value
