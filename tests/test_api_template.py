from config import Config

from app.commons.exceptions import _StatusCode, _ErrorStatus, ErrorMessage


def test_response_format(client):
    response, data = client.get('/api/v1/tests')

    assert data.get('status') is not None
    assert data.get('message') is not None
    assert data.get('data') is not None
    assert data.get('_meta') is not None
    assert data.get('_meta').get('service_name') == Config.SERVICE_NAME


def test_no_post_data(client):
    response, data = client.post('/api/v1/tests')

    assert response.status_code == _StatusCode.BAD_REQUEST
    assert data.get('status') == _ErrorStatus.FAILURE
    assert data.get('message') == ErrorMessage.EMPTY_POST_DATA


def test_no_required_params(client):
    payload = {
        'test1': 'test',
    }

    response, data = client.post('/api/v1/tests', data=payload)

    assert response.status_code == _StatusCode.BAD_REQUEST
    assert data.get('status') == _ErrorStatus.FAILURE
    assert 'is required' in data.get('message')


def test_empty_required_params(client):
    payload = {
        'test1': 'test',
        'test2': ''
    }

    response, data = client.post('/api/v1/tests', data=payload)

    assert response.status_code == _StatusCode.BAD_REQUEST
    assert data.get('status') == _ErrorStatus.FAILURE
    assert 'is required' in data.get('message')
