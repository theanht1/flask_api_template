from app.commons.api_template import BaseGetRequestTemplate, BasePostRequestTemplate


class GetRequestTemplateV2(BaseGetRequestTemplate):
    def __init__(self, request_data={}):
        """
        Include api version to the response data

        :param request_data:
        """
        super().__init__(request_data)

        self.response_meta_data = {
            'api_version': '2'
        }

    def main_logic(self):
        super().main_logic()


class PostRequestTemplateV2(BasePostRequestTemplate):
    def __init__(self, request_data={}):
        """
        Include api version to the response data

        :param request_data:
        """
        super().__init__(request_data)

        self.response_meta_data = {
            'api_version': '2'
        }

    def main_logic(self):
        super().main_logic()
