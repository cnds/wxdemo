from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class PaymentDetail(Base):

    """
    先计算折扣和满减，然后根据用户的积分情况，获取优惠券情况，计算出实际需要支付的金额

    所有优惠都在最开始都金额基础上做计算
    """

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
            if actual_amount >= discount_minus:
                result.update({'discount': {'base': discount_base,
                                            'minus': discount_minus}})
                actual_amount -= discount_minus

        flag, points = self.db.find_by_condition(
            'points', {'userId': user_id, 'storeId': store_id})
        if not flag:
            return '', 500

        if points:
            point = points[0]['point']
            flag, coupons = self.db.find_by_condition(
                'coupons', {'storeId': store_id, 'point': {'$lte': point}})
            if not flag:
                return '', 500

            if coupons:
                coupon_point = coupons[0]['point']
                coupon_minus = coupons[0]['minus']
                for coupon in coupons:
                    if coupon['point'] > coupon_point:
                        coupon_point = coupon['point']
                        coupon_minus = coupon['minus']
                if actual_amount >= coupon_minus:
                    result.update({'coupon': {'point': coupon_point,
                                              'minus': coupon_minus}})
                    actual_amount -= coupon_minus

        result.update({'actualAmount': actual_amount})
        return jsonify(result), 201

