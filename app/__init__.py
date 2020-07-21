from flask import Flask, request
from flask_cors import CORS

from app.commons.exceptions import InvalidUsage, NotAllowed, NotFound, Unauthorized
from config.development import DevelopmentConfig
from config.production import ProductionConfig
from config.test import TestConfig

# Configs
configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "test": TestConfig,
}


def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)
    # CORS
    CORS(app)

    # Apply configuration
    app.config.from_object(configs.get(config_name))

    # Register blueprints
    from .controllers import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    # Hello endpoint
    @app.route("/hello", methods=["GET"])
    def hello():
        return "Hello"

    # Handle request events
    @app.before_request
    def handle_before_request():
        # Allow the pre-flight requests to get through
        if request.method == "OPTIONS":
            return None

    @app.errorhandler(401)
    def unauthorized(error):
        return Unauthorized(message="Bad username or password",).to_response()

    @app.errorhandler(404)
    def not_found(error):
        return NotFound(message="Resource was not found",).to_response()

    @app.errorhandler(405)
    def not_allowed(error):
        return NotAllowed(message="Method was not allowed",).to_response()

    @app.errorhandler(InvalidUsage)
    def invalid_usage(error: InvalidUsage):
        return error.to_response()

    return app
