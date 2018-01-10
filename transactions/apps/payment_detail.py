from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class PaymentDetail(Base):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['payment_detail_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'])

        store_id = data['storeId']
        user_id = data['userId']
        amount = data['amount']
        actual_amount = amount
        result = dict()

        flag, reduction = self.db.find_by_condition('reductions',
                                                    {'storeId', store_id})
        if not flag:
            return '', 500

        if reduction:
            reduction = reduction[0]
            result.update({'reduction': reduction})
            actual_amount = actual_amount * reduction['percent'] / 100

        flag, discount = self.db.find_by_condition('discounts',
                                                   {'storeId': store_id})
        if not flag:
            return '', 500

        if discount:
            discount = discount[0]
            discount_base = discount['base']
            discount_minus = discount['minus']
            result.update({'discount': discount})
            if amount >= discount_base:
                actual_amount = actual_amount - discount_minus

        flag, user_coupons = self.db.find_by_condition(
            'userCoupons', {'storeId': store_id, 'userId': user_id})
        if not flag:
            return '', 500

        if user_coupons:
            coupon_id_list = user_coupons['coupons']
            flag, coupons = self.db.find_by_condition('coupons', {'id': {
                '$in': coupon_id_list}, 'base': {'$lte': amount}})
            if not flag:
                return '', 500

            if coupons:
                result.update({'coupons': coupons[0]})
                for coupon in coupons:
                    if coupon['base'] > result['coupons']['base']:
                        result['coupons'].update(coupon)

                coupon_minus = result['coupon']['minus']
                actual_amount = actual_amount - coupon_minus

        result.update({'actualAmount': actual_amount})
        return jsonify({'paymentDetail': result})

