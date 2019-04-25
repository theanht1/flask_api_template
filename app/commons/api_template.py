from flask import request, jsonify, current_app
from app.commons.exceptions import ErrorMessage, InvalidUsage

from config import Config


class ServiceInvalidUsage(InvalidUsage):
    def __init__(self, message, status_code=None, status_message=None, payload=None):
        """
        Include _meta response data into the response of the exception

        :param message: <string>
        :param status_code: <number>
        :param status_message: <string>
        :param payload: <dict>
        """
        _payload = dict(payload or ())
        _payload['_meta'] = {
            'service_name': current_app.config['SERVICE_NAME']
        }

        super().__init__(message=message, status_code=status_code, status_message=status_message, payload=_payload)


# Template class for POST request
class BasePostRequestTemplate:
    def __init__(self, request_data={}):
        """
        Response format:
        {
            "_meta": {
                "service_name": ""
            },
            "data": {},
            "message": ""
            "status": ""
        }
        :param request_data: <dict>
        """
        self.request_data = request_data.copy()  # JSON request data
        self.response_data = None  # Main response data
        self.response_meta_data = None  # Meta information
        self.response_status_code = 200  # HTTP response status code
        self.response_status = 'SUCCESS'  # Response status text
        self.response_message = ''  # Response message

    def _validate_request(self, required_params=[], optional_params=[]):
        """
        Check format, datatype of the JSON request data (application/json) and preprocess it.

        :param required_params: <list> list of required parameters
        :param optional_params: <list> list of optional parameters
        :return:
        """
        req_data: dict = request.get_json(silent=True)

        if req_data is None:
            raise ServiceInvalidUsage(message=ErrorMessage.EMPTY_POST_DATA)
        else:
            # Validate request data & process data
            for param in required_params:
                value = req_data.get(param)

                # Check if required param is missing
                if value is None or value == "":
                    raise ServiceInvalidUsage(message="'{}' is required".format(param))
                else:
                    self.request_data[param] = value

            # Process the optional parameters
            for param in optional_params:
                self.request_data[param] = req_data.get(param)

    def main_logic(self):
        """Process the message in the request
        This function must set the response_data and response_message instance
        variables
        """
        raise NotImplementedError()

    def _format_response_data(self):
        """
        Reformat the http response data before send it to the client

        :return: Json http response
        """
        response = {
            'status': self.response_status,
            'message': self.response_message,
            'data': self.response_data,
            '_meta': {
                'service_name': Config.SERVICE_NAME
            }
        }

        if self.response_meta_data is not None:
            for meta in self.response_meta_data:
                response['_meta'][meta] = self.response_meta_data.get(meta)

        return jsonify(response)

    def request_handler(self, required_params=[], optional_params=[]):
        """
        Main method to execute the template

        :param required_params: <list>
        :param optional_params: <list>
        :return:
        """

        self._validate_request(required_params, optional_params)
        self.main_logic()
        return self._format_response_data(), self.response_status_code


# Template class for GET request
class BaseGetRequestTemplate:
    def __init__(self, request_data={}):
        """
        Response format:
        {
            "_meta": {
                "service_name": ""
            },
            "data": {},
            "message": ""
            "status": ""
        }
        :param request_data: <dict>
        """
        self.request_data = request_data
        self.response_data = None
        self.response_meta_data = None
        self.response_status_code = 200
        self.response_status = 'SUCCESS'
        self.response_message = ''

    def _validate_request(self, required_params=[], optional_params=[]):
        """
        Check format, datatype of the JSON request data (application/json) and preprocess it.

        :param required_params: <list> list of required parameters
        :param optional_params: <list> list of optional parameters
        :return:
        """

        # Validate request data & process data
        for param in required_params:
            value = request.args.get(param)

            # Check if required param is missing
            if value is None or value == "":
                raise ServiceInvalidUsage(message="'{}' is required".format(param))
            else:
                self.request_data[param] = value

        # Process the optional parameters
        for param in optional_params:
            self.request_data[param] = request.args.get(param)

    def _format_response_data(self):
        """
        Reformat the http response data before send it to the client

        :return: Json http response
        """

        response = {
            'status': self.response_status,
            'message': self.response_message,
            'data': self.response_data,
            '_meta': {
                'service_name': Config.SERVICE_NAME
            }
        }

        if self.response_meta_data is not None:
            for meta in self.response_meta_data:
                response['_meta'][meta] = self.response_meta_data.get(meta)

        return jsonify(response)

    def main_logic(self):
        """
        This method process the main logic to set the response_data and response_message
        :return:
        """
        raise NotImplementedError()

    def request_handler(self, required_params=[], optional_params=[]):
        """
        Main method to execute the template

        :param required_params: <list>
        :param optional_params: <list>
        :return:
        """
        self._validate_request(required_params, optional_params)
        self.main_logic()
        return self._format_response_data(), self.response_status_code
