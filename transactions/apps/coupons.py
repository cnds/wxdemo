from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class Coupons(Base):

    def get(self):
        params = request.args.to_dict()
        flag, tag = self.validate_dict_with_schema(params,
                                                   SCHEMA['coupons_get'])
        if not flag:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        flag, coupons = self.db.find_by_condition('coupons', params)
        if not flag:
            return '', 500

        return jsonify({'coupons': coupons})

    def post(self):
        is_valid, data =self.get_params_from_request(request,
                                                     SCHEMA['coupons_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        condition = self.get_data_with_keys(data,
                                            ('storeId', 'pay', 'base', 'minus'))
        flag, coupon = self.db.find_by_condition('coupons', condition)
        if not flag:
            return '', 500

        if coupon:
            return self.error_msg(self.ERR['conflict_coupon'])

