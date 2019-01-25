from flask import Flask, request
from flask_cors import CORS

from .config import configuration
from .resources import SERVICE_NAME, load_all_resources
from .commons.exceptions import NotFound, NotAllowed, InvalidUsage, Unauthorized

# Init application
app = Flask(__name__)
app.config.from_object(configuration)

# setup cross-domain
CORS(app=app)


# Handle request events
@app.before_request
def handle_before_request():
    # Allow the pre-flight request to get through
    if request.method == 'OPTIONS':
        return None


# Handle request errors
common_payload = {
    '_meta': {
        'service_name': SERVICE_NAME
    }
}


@app.errorhandler(401)
def unauthorized(error):
    return Unauthorized(
        message="Bad username or password",
        payload=common_payload
    ).to_response()


@app.errorhandler(404)
def not_found(error):
    return NotFound(
        message="Resource was not found",
        payload=common_payload
    ).to_response()


@app.errorhandler(405)
def not_allowed(error):
    return NotAllowed(
        message="Method was not allowed",
        payload=common_payload
    ).to_response()


@app.errorhandler(InvalidUsage)
def invalid_usage(error):
    return error.to_response()


# Load endpoints for the API
load_all_resources()
