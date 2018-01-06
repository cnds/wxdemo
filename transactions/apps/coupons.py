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
        is_valid, data = self.get_params_from_request(request,
                                                      SCHEMA['coupons_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        condition = self.get_data_with_keys(data,
                                            ('storeId', 'pay', 'base'))
        flag, coupon = self.db.find_by_condition('coupons', condition)
        if not flag:
            return '', 500

        if coupon:
            return self.error_msg(self.ERR['conflict_coupon'])

        result = self.db.create('coupons', data)
        if not result:
            return '', 500

        return jsonify(result)


class Coupon(Base):

    def get(self, coupon_id):
        flag, coupon = self.db.find_by_id('coupons', coupon_id)
        if not flag:
            return '', 500

        if coupon is None:
            return self.error_msg(self.ERR['coupon_not_exist'])

        return jsonify(coupon)

    def put(self, coupon_id):
        is_valid, data = self.get_params_from_request(request,
                                                      SCHEMA['coupon_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        flag, result = self.db.update('coupons', {'id': coupon_id},
                                      {'$set': data})
        if not flag:
            return '', 500

        return jsonify(result)

    def delete(self, coupon_id):
        flag, result = self.db.remove('coupons', coupon_id)
        if not flag:
            return '', 500

        if result is None:
            return self.error_msg(self.ERR['coupon_has_been_removed'])

        return jsonify(result)

