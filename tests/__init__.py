import json
from base64 import b64encode


class AppTestClient:
    def __init__(self, app, username, password):
        self.client = app.test_client()
        self.auth = 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')

    def send(self, url, request, data=None, headers=None):
        if not headers:
            headers = {}
        headers['Authorization'] = self.auth
        headers['Content-Type'] = 'application/json'

        # Convert json data to string
        data = json.dumps(data) if data else None

        rv = request(url, data=data, headers=headers)

        return rv, json.loads(rv.data.decode('utf-8'))

    def get(self, url, headers=None):
        return self.send(url, self.client.get, headers=headers)

    def post(self, url, data=None, headers=None):
        return self.send(url, self.client.post, data=data, headers=headers)

    def put(self, url, data=None, headers=None):
        return self.send(url, self.client.put, data=data, headers=headers)

    def delete(self, url, headers=None):
        return self.send(url, self.delete, headers=headers)
