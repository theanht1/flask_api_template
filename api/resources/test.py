"""
This module is only for unit testing
"""
from api.app import app
from api.commons.decorators.authentication import required_basic_authentication

from . import END_POINT_URI, GetRequestTemplate, PostRequestTemplate

__resource_name__ = 'tests'


class GetTest(GetRequestTemplate):
    def main_logic(self):
        self.response_message = 'Tested successfully'
        self.response_data = {
            'message': 'Just for testing'
        }


class PostTest(PostRequestTemplate):
    def main_logic(self):
        self.response_message = "Tested successfully"
        self.response_data = {
            'message': 'Just for testing post method'
        }


@app.route(END_POINT_URI + __resource_name__, methods=['GET'])
@required_basic_authentication()
def get_test():
    test = GetTest()

    return test.request_handler()


@app.route(END_POINT_URI + __resource_name__, methods=['POST'])
def post_test():
    test = PostTest()

    required_params = ['test1', 'test2']
    optional_params = ['opt_test1']

    return test.request_handler(required_params, optional_params)
