"""
This module is only for unit testing
"""

from app.commons.decorators.authentication import required_basic_authentication
from app.commons.decorators.request_parsers import parse_args_with
from app.controllers import api
from app.schemas.base import BaseResponse, TestRequest, TestResponse

__resource_name__ = '/tests'


@api.route('{}'.format(__resource_name__), methods=['GET'])
@required_basic_authentication
def get_test():
    return BaseResponse().jsonify()


@api.route('{}'.format(__resource_name__), methods=['POST'])
@required_basic_authentication
@parse_args_with(TestRequest())
def post_test(args):
    return TestResponse().jsonify(args)
