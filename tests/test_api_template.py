from app.commons.exceptions import ErrorMessage, ErrorStatus, StatusCode


def test_response_format(client):
    response, data = client.get("/api/v1/tests")

    assert response.status_code == StatusCode.SUCCESS
    assert data.get("data") is not None


def test_no_post_data(client):
    response, data = client.post("/api/v1/tests")

    assert response.status_code == StatusCode.BAD_REQUEST
    assert data.get("status") == ErrorStatus.FAILURE
    assert data.get("message") == ErrorMessage.INVALID_POST_DATA


def test_no_required_params(client):
    payload = {
        "arg2": "arg2",
    }

    response, data = client.post("/api/v1/tests", data=payload)

    assert response.status_code == StatusCode.BAD_REQUEST
    assert data.get("status") == ErrorStatus.FAILURE
    assert data.get("message") == ErrorMessage.INVALID_POST_DATA


def test_post_success(client):
    payload = {
        "arg1": "arg1",
        "arg2": "arg12",
    }

    response, data = client.post("/api/v1/tests", data=payload)

    assert response.status_code == StatusCode.SUCCESS
    assert data["data"] == payload
