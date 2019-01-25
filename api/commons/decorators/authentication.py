import base64
import re

from functools import wraps
from flask import request
from werkzeug.exceptions import Unauthorized


def required_basic_authentication():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            authentication_header = request.headers.get('Authorization')
            if not authentication_header:
                raise Unauthorized()

            # Get authentication info
            try:
                authentication_str = re.split('^Basic ', authentication_header)[1]
                authentication_decoded = base64.b64decode(authentication_str).decode('utf-8')

                username, password = authentication_decoded.split(':')

            except (IndexError, ValueError):
                raise Unauthorized()

            # Check the validation of the pair of username and password
            if not mongo_utils.check_authentication(username, password):
                raise Unauthorized()

            return f(*args, **kwargs)

        return decorated_function

    return decorator
