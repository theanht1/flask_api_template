import pytest

from app import create_app

from . import AppTestClient


@pytest.fixture
def app():
    app = create_app("test")

    # Create and load test data
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return AppTestClient(app, app.config["USERNAME"], app.config["PASSWORD"])
