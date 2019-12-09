import json

from app.commons.enums import ErrorStatus, StatusCode


def test_success(app):
    response = app.test_client().get('/hello')

    assert response.status_code == 200
    assert response.data == b'Hello'


def test_authentication(app):
    response = app.test_client().get('/api/v1/tests')

    assert response.status_code == StatusCode.UNAUTHORIZED
    assert json.loads(response.data)['status'] == ErrorStatus.UNAUTHORIZED


def test_resource_not_found(client):
    response, data = client.get('/dummy')

    assert response.status_code == StatusCode.NOT_FOUND
    assert data['status'] == ErrorStatus.NOT_FOUND


def test_method_not_allowed(client):
    response, data = client.put('/api/v1/tests')

    assert response.status_code == StatusCode.NOT_ALLOWED
    assert data.get('status') == ErrorStatus.NOT_ALLOWED
