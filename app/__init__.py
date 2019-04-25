import os
from flask import Flask, request

from app.libs.mysql_wrapper import MySQLWrapper
from app.commons.exceptions import NotAllowed, NotFound, InvalidUsage, Unauthorized
from config import Config as DefaultConfig

# Create mysql connection instance
mysql_db = MySQLWrapper()


def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # Apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_object(DefaultConfig)  # Default settings
    app.config.from_pyfile(cfg)

    # Setup database
    mysql_db.init_app(app)

    # Register blueprints
    from .api_v1 import api as api_blueprint
    from .api_v2 import api as api_blueprint2

    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.register_blueprint(api_blueprint2, url_prefix='/api/v2')

    # Hello endpoint
    @app.route('/hello', methods=['GET'])
    def hello():
        return 'Hello, Got It'

    # Handle request events
    @app.before_request
    def handle_before_request():
        # Allow the pre-flight requests to get through
        if request.method == 'OPTIONS':
            return None

    # Handle request errors
    common_payload = {
        '_meta': {
            'service_name': DefaultConfig.SERVICE_NAME
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
    def invalid_usage(error: InvalidUsage):
        return error.to_response()

    return app
