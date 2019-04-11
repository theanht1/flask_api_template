import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app('testing')

    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
