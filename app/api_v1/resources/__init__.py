from app.commons.api_template import BaseGetRequestTemplate, BasePostRequestTemplate


class GetRequestTemplateV1(BaseGetRequestTemplate):
    def __init__(self, request_data={}):
        super().__init__(request_data)

        self.response_meta_data = {
            'api_version': '1'
        }

    def main_logic(self):
        super().main_logic()


class PostRequestTemplateV1(BasePostRequestTemplate):
    def __init__(self, request_data={}):
        super().__init__(request_data)

        self.response_meta_data = {
            'api_version': '1'
        }

    def main_logic(self):
        super().main_logic()
