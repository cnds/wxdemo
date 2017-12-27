from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class ActualAmount(Base):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['actual_amount_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'])

        store_id = data['storeId']
        user_id = data['userId']
        amount = data['amount']

        flag, promotion = self.db.find_by_condition('promotions',
                                                    {'storeId', store_id})
        if not flag:
            return '', 500

        if not promotion:
            return jsonify({'actualAmount': amount})

        promotion = promotion[0]
        discount = promotion['discount']
        discount_base = discount['base']
        discount_minus = discount['minus']
        if amount >= discount_base:
            actual_amount = amount - discount_minus
        else:
            actual_amount = amount

        # NOTE: coupon collection need to be optimized
        flag, coupon = self.db.find_by_condition('coupon', {
            'storeId': store_id, 'userId': user_id})
        if not flag:
            return '', 500

        if not coupon:
            return jsonify({'actualAmount': actual_amount})

        coupon = coupon[0]
        if coupon['number'] == 0:
            return jsonify({'actualAmount': actual_amount})

        coupon_base = coupon['base']
        coupon_minus = coupon['minus']
        if amount >= coupon_base:
            actual_amount = actual_amount - coupon_minus

        return jsonify({'actualAmount': actual_amount})

