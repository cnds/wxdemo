from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class PaymentDetail(Base):
    """
    先查店铺优惠(discounts, reductions)，再查自己的优惠券(userCoupons)，然后叠加生成实际金额。
    """
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
            # NOTE: compare amount and coupons base, get nearest nearest base and use it.
            coupons_can_use = [coupon for coupon in user_coupons['coupons']
                               if coupon['base'] <= amount]
            for i, coupon in enumerate(coupons_can_use):
                if i == 0:
                    result.update({'coupon': coupon})
                else:
                    if coupon['base'] < result['coupon']['base']:
                        result.update({'coupon': coupon})

            coupon_base = result['coupon']['base']
            coupon_minus = result['coupon']['minus']
            if amount >= coupon_base:
                actual_amount = actual_amount - coupon_minus

        result.update({'actualAmount': actual_amount})
        return jsonify({'paymentDetail': result})

