from functools import wraps

from flask import request
from marshmallow import ValidationError

from app import InvalidUsage
from app.commons.enums import ErrorMessage


def parse_args_with(schema):
    """ Decorator for parsing request data with marshmallow schema """

    def parse_args_with_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == "GET":
                request_args = request.args.to_dict()
            else:
                request_args = request.get_json(silent=True) or {}

            try:
                parsed_args = schema.load(request_args)
                kwargs["args"] = parsed_args
            except ValidationError as error:
                raise InvalidUsage(
                    ErrorMessage.INVALID_POST_DATA, error_data=error.messages
                )
            return f(*args, **kwargs)

        return decorated_function

    return parse_args_with_decorator
