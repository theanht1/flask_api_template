import base64
import re

from functools import wraps
from flask import current_app, request
from werkzeug.exceptions import Unauthorized


def _validate_basic_authentication(username, password):
    """
    Check the validation of the username, password pair.

    :param username: <string> http basic authentication user name
    :param password: <string> http basic authentication password
    :return:
    """
    correct_username = current_app.config['USERNAME']
    correct_password = current_app.config['PASSWORD']

    return username == correct_username and password == correct_password


# Decorator to check the basic http authentication of the request
def required_basic_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authentication_header = request.headers.get('Authorization')
        if not authentication_header:
            raise Unauthorized()

        # Get authentication info
        try:
            # Extract the username and password form the request authorization header by remove prefix and decode it
            authentication_str = re.split('^Basic ', authentication_header)[1]
            authentication_decoded = base64.b64decode(authentication_str).decode('utf-8')

            username, password = authentication_decoded.split(':')

        except (IndexError, ValueError):
            raise Unauthorized()

        # Check the validation of the pair of username and password
        if not _validate_basic_authentication(username, password):
            raise Unauthorized()

        return f(*args, **kwargs)

    return decorated_function
