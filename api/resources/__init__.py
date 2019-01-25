from flask import request, jsonify
from api.commons.exceptions import ErrorMessage, InvalidUsage

END_POINT_URI = '/v1/'
SERVICE_NAME = 'seo_platform'


def load_all_resources():
    #  TODO: Include the api resources here
    from api.resources import test


class ServiceInvalidUsage(InvalidUsage):
    def __init__(self, message, status_code=None, status_message=None, payload=None):
        _payload = dict(payload or ())
        _payload['_meta'] = {
            'service_name': SERVICE_NAME
        }
        super().__init__(message=message, status_code=status_code, status_message=status_message, payload=_payload)


# Template class for POST request
class PostRequestTemplate:
    def __init__(self, request_data={}):
        self.request_data = request_data
        self.response_data = None
        self.response_status_code = 200
        self.response_status = 'SUCCESS'
        self.response_message = ''

    def _validate_request(self, required_params=[], optional_params=[]):
        req_data: dict = request.get_json()

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
        return jsonify({
            'status': self.response_status,
            'message': self.response_message,
            'data': self.response_data,
            '_meta': {
                'service_name': SERVICE_NAME
            }
        })

    def request_handler(self, required_params=[], optional_params=[]):
        self._validate_request(required_params, optional_params)
        self.main_logic()
        return self._format_response_data(), self.response_status_code


# Template class for GET request
class GetRequestTemplate:
    def __init__(self, request_data={}):
        self.request_data = request_data
        self.response_data = None
        self.response_meta_data = None
        self.response_status_code = 200
        self.response_status = 'SUCCESS'
        self.response_message = ''

    def _validate_request(self, required_params=[], optional_params=[]):
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
        response = {
            'status': self.response_status,
            'message': self.response_message,
            'data': self.response_data,
            '_meta': {
                'service_name': SERVICE_NAME
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
        self._validate_request(required_params, optional_params)
        self.main_logic()
        return self._format_response_data(), self.response_status_code
