import os, sys
import json
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

os.environ['SEO_PLATFORM'] = 'testing'

from api.commons.exceptions import ErrorMessage, _StatusCode, _ErrorStatus
from api.app import app


class ErrorHttpTestCase(unittest.TestCase):
    """
    Test the error status of the http request
    """

    def setUp(self):
        self.uri = '/v1/'
        self.app = app.test_client()

    def _request(self, resource, request, data=None, content_type=None):
        rv = request(self.uri + resource, data=data, content_type=content_type)
        res_data = json.loads(rv.data.decode('utf-8'))

        return rv, res_data

    def test_post_susccess(self):
        resource = 'tests'

        payload = {
            'test1': '1',
            'test2': '2',
        }

        rv, res_data = self._request(resource, self.app.post, data=json.dumps(payload), content_type='application/json')

        self.assertEqual(200, rv.status_code)
        self.assertEqual("SUCCESS", res_data.get('status'))

    def test_not_found_resource(self):
        rv = self.app.get('/test_resource')
        res_data = json.loads(rv.data.decode('utf-8'))

        self.assertEqual(_StatusCode.NOT_FOUND, rv.status_code)
        self.assertEqual(_ErrorStatus.NOT_FOUND, res_data.get('status'))

    def test_not_allowed_method(self):
        resource = 'tests'

        rv, res_data = self._request(resource, self.app.delete)

        self.assertEqual(_StatusCode.NOT_ALLOWED, rv.status_code)
        self.assertEqual(_ErrorStatus.NOT_ALLOWED, res_data.get('status'))

    def test_not_post_data(self):
        resource = 'tests'

        rv, res_data = self._request(resource, self.app.post)

        self.assertEqual(_StatusCode.BAD_REQUEST, rv.status_code)
        self.assertEqual(_ErrorStatus.FAILURE, res_data.get('status'))
        self.assertEqual(ErrorMessage.EMPTY_POST_DATA, res_data.get('message'))

    def test_miss_required_param(self):
        resource = 'tests'

        # Missing timestamp field
        payload = {
            'test1': '1',
        }

        rv, res_data = self._request(resource, self.app.post, data=json.dumps(payload), content_type='application/json')

        self.assertEqual(_StatusCode.BAD_REQUEST, rv.status_code)
        self.assertEqual(_ErrorStatus.FAILURE, res_data.get('status'))
        self.assertEqual("'test2' is required", res_data.get('message'))

    def test_empty_required_param(self):
        resource = 'tests'

        # Timestamp field is empty
        payload = {
            'test1': '1',
            'test2': '',
        }

        rv, res_data = self._request(resource, self.app.post, data=json.dumps(payload), content_type='application/json')

        self.assertEqual(_StatusCode.BAD_REQUEST, rv.status_code)
        self.assertEqual(_ErrorStatus.FAILURE, res_data.get('status'))
        self.assertEqual("'test2' is required", res_data.get('message'))


if __name__ == '__main__':
    unittest.main()
