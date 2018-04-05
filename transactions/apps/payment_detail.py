from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class PaymentDetail(Base):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['payment_detail_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        store_id = data['storeId']
        user_id = data['userId']
        amount = data['amount']
        actual_amount = amount
        result = dict()

        flag, reduction = self.db.find_by_condition('reductions',
                                                    {'storeId': store_id})
        if not flag:
            return '', 500

        if reduction:
            reduction = reduction[0]
            percent = reduction['percent']
            result.update({'reduction': {'percent': percent}})
            actual_amount = actual_amount * percent / 100

        flag, discounts = self.db.find_by_condition('discounts',
                                                   {'storeId': store_id,
                                                    'base': {'$lte': amount}})
        if not flag:
            return '', 500

        if discounts:
            discount_base = discounts[0]['base']
            discount_minus = discounts[0]['minus']
            for discount in discounts:
                if discount['base'] > discount_base:
                    discount_base = discount['base']
                    discount_minus = discount['minus']
            result.update({'discount': {'base': discount_base,
                                        'minus': discount_minus}})
            actual_amount -= discount_minus

        flag, user_coupons = self.db.find_by_condition(
            'userCoupons', {'storeId': store_id, 'userId': user_id})
        if not flag:
            return '', 500

        if user_coupons:
            from bson import ObjectId
            coupon_id_list = [ObjectId(coupon_id) for coupon_id
                              in user_coupons[0]['coupons'].keys()]
            # coupon_id_list = [ObjectId(coupon_id) for coupon_id
            #                   in user_coupons[0]['coupons']]
            flag, coupons = self.db.find_by_condition('coupons', {'_id': {
                '$in': coupon_id_list}, 'base': {'$lte': amount}})
            if not flag:
                return '', 500

            if coupons:
                coupon_base = coupons[0]['base']
                coupon_minus = coupons[0]['minus']
                coupon_pay = coupons[0]['pay']
                coupon_id = coupons[0]['id']
                for coupon in coupons:
                    if coupon['base'] > coupon_base:
                        coupon_base = coupon['base']
                        coupon_minus = coupon['minus']
                        coupon_pay = coupon['pay']
                        coupon_id = coupon['id']

                result.update({'coupon': {'pay': coupon_pay,
                                          'base': coupon_base,
                                          'minus': coupon_minus,
                                          'id': coupon_id}})
                actual_amount = actual_amount - coupon_minus

        result.update({'actualAmount': actual_amount})
        return jsonify(result), 201

