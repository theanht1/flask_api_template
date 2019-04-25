from flask import jsonify, make_response


class _StatusCode:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    NOT_ALLOWED = 405


class _ErrorStatus:
    NOT_FOUND = "NOT FOUND"
    NOT_ALLOWED = "METHOD WAS NOT ALLOWED"
    FAILURE = "FAILURE"
    UNAUTHORIZED = "UNAUTHORIZED"


class ErrorMessage:
    EMPTY_POST_DATA = 'POST data is required'
    ERROR = "ERROR"


class _BaseException(Exception):
    status_code = 0
    status_message = ErrorMessage.ERROR

    def __init__(self, message, status_code=None, status_message=None, payload=None):
        """
        Customize the response exception

        :param message: <string> Message field in the response body
        :param status_code: <number> HTTP status code
        :param status_message: <string> Status text for the response
        :param payload: <dict> Json body data
        """
        self.message = message

        if status_code is not None:
            self.status_code = status_code

        if status_message is not None:
            self.status_message = status_message

        self.payload = payload

    def to_dict(self):
        """
        Convert the response to dictionary format
        :return:
        """
        rv = dict(self.payload or ())
        rv['message'] = self.message

        if self.status_message is not None:
            rv['status'] = self.status_message

        return rv

    def to_response(self):
        """
        Response to client Json format
        :return:
        """
        resp = jsonify(self.to_dict())

        return make_response(resp, self.status_code)


class NotFound(_BaseException):
    """
    404 Not Found
    """
    status_code = _StatusCode.NOT_FOUND
    status_message = _ErrorStatus.NOT_FOUND


class NotAllowed(_BaseException):
    """
    405 Method Not Allowed
    """
    status_code = _StatusCode.NOT_ALLOWED
    status_message = _ErrorStatus.NOT_ALLOWED


class InvalidUsage(_BaseException):
    """
    400 Bad request
    """
    status_code = _StatusCode.BAD_REQUEST
    status_message = _ErrorStatus.FAILURE


class Unauthorized(_BaseException):
    """
    401 Unauthorized request
    """
    status_code = _StatusCode.UNAUTHORIZED
    status_message = _ErrorStatus.UNAUTHORIZED
