import base64
import re

from functools import wraps
from flask import current_app, request
from werkzeug.exceptions import Unauthorized


def _validate_basic_authentication(username, password):
    # TODO: Implement this method
    correct_username = current_app.config['USERNAME']
    correct_password = current_app.config['PASSWORD']

    return username == correct_username and password == correct_password


def required_basic_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authentication_header = request.headers.get("Authorization")
        if not authentication_header:
            raise Unauthorized()

        # Get authentication info
        try:
            authentication_str = re.split('^Basic ', authentication_header)[1]
            authentication_decoded = base64.b64decode(authentication_str).decode('utf-8')

            username, password = authentication_decoded.split(":")

        except (IndexError, ValueError):
            raise Unauthorized()

        # Check the validation of the pair of username and password
        if not _validate_basic_authentication(username, password):
            raise Unauthorized()

        return f(*args, **kwargs)

    return decorated_function
