from flask import jsonify, make_response

from app.commons.enums import ErrorMessage, StatusCode, ErrorStatus


class _BaseException(Exception):
    status_code = 0
    status_message = ErrorMessage.ERROR

    def __init__(self, message, status_code=None, status_message=None, error_data=None, payload=None):
        """
        Customize the response exception

        :param message: <string> Message field in the response body
        :param status_code: <number> HTTP status code
        :param status_message: <string> Status text for the response
        :param error_data: <dict|list|string>
        :param payload: <dict> Json body data
        """
        self.message = message

        if status_code is not None:
            self.status_code = status_code

        if status_message is not None:
            self.status_message = status_message

        self.error_data = error_data
        self.payload = payload

    def to_dict(self):
        """
        Convert the response to dictionary format
        :return:
        """
        rv = dict(self.payload or ())
        rv['message'] = self.message

        if self.error_data:
            rv['error_data'] = self.error_data

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
    status_code = StatusCode.NOT_FOUND
    status_message = ErrorStatus.NOT_FOUND


class NotAllowed(_BaseException):
    """
    405 Method Not Allowed
    """
    status_code = StatusCode.NOT_ALLOWED
    status_message = ErrorStatus.NOT_ALLOWED


class InvalidUsage(_BaseException):
    """
    400 Bad request
    """
    status_code = StatusCode.BAD_REQUEST
    status_message = ErrorStatus.FAILURE


class Unauthorized(_BaseException):
    """
    401 Unauthorized request
    """
    status_code = StatusCode.UNAUTHORIZED
    status_message = ErrorStatus.UNAUTHORIZED
