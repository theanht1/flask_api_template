from base64 import b64encode
import json


class TestClient():
    def __init__(self, app, username, password):
        self.app = app
        self.auth = 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
