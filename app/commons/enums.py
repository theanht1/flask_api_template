class StatusCode:
    SUCCESS = 200
    CREATED = 201
    NO_CONTENT = 204

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    NOT_ALLOWED = 405


class ErrorStatus:
    NOT_FOUND = "NOT FOUND"
    NOT_ALLOWED = "METHOD WAS NOT ALLOWED"
    FAILURE = "FAILURE"
    UNAUTHORIZED = "UNAUTHORIZED"


class ErrorMessage:
    INVALID_POST_DATA = 'Invalid request data'
    ERROR = "ERROR"
