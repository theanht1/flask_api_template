"""
This module is only for unit testing
"""

from . import GetRequestTemplateV1, PostRequestTemplateV1

from app.commons.decorators.authentication import required_basic_authentication

from .. import api

__resource_name__ = '/tests'


# --- Models to handle api endpoints ---

class GetTest(GetRequestTemplateV1):
    """
    Test /GET request
    """

    def main_logic(self):
        self.response_message = 'Tested successfully'
        self.response_data = {
            'message': 'Just for testing'
        }


class PostTest(PostRequestTemplateV1):
    """
    Test /POST request
    """

    def main_logic(self):
        self.response_message = 'Tested successfully'
        self.response_data = {
            'message': 'Just for testing post method'
        }


# --- API endpoints ---

@api.route('{}'.format(__resource_name__), methods=['GET'])
@required_basic_authentication
def get_test():
    test = GetTest()

    return test.request_handler()


@api.route('{}'.format(__resource_name__), methods=['POST'])
def post_test():
    test = PostTest()

    required_params = ['test1', 'test2']
    optional_params = ['opt_test1']

    return test.request_handler(required_params=required_params, optional_params=optional_params)
