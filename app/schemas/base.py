from flask import jsonify
from marshmallow import Schema, fields, post_dump


class PaginationSchema(Schema):
    page = fields.Integer(validate=lambda n: n >= 1, required=False, default=1)
    items_per_page = fields.Integer(
        validate=lambda n: n >= 1, required=False, default=10
    )


class BaseResponse(Schema):
    @post_dump(pass_many=True)
    def wrap(self, data, many):
        return {
            "data": data,
        }

    def jsonify(self, obj=None, many=False):
        if not obj:
            obj = {}
        return jsonify(self.dump(obj, many=many))


class TestRequest(Schema):
    arg1 = fields.String(required=True)
    arg2 = fields.String(required=False)


class TestResponse(BaseResponse):
    arg1 = fields.String(required=True)
    arg2 = fields.String(required=False)
