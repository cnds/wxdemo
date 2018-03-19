from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class UserCoupons(Base):
    def get(self):
        """
        {
            "userCoupons": [
                {
                    "userId": xxx,
                    "storeId": yyy,
                    "coupons": []
                },
                {
                    "userId": aaa,
                    "storeId": bbb,
                    "coupons": []
                }
            ]
        }
        """
        params = request.args.to_dict()
        is_valid, tag = self.validate_dict_with_schema(
            params, SCHEMA['user_coupons_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        flag, user_coupons = self.db.find_by_condition('userCoupons', params)
        if not flag:
            return '', 500

        if user_coupons:
            print(user_coupons)
            for user_coupon in user_coupons:
                from bson import ObjectId
                coupon_id_list = [ObjectId(coupon_id) for coupon_id
                                  in user_coupon['coupons']]
                flag, coupons = self.db.find_by_condition(
                    'coupons', {'_id': {'$in': coupon_id_list}})
                if not flag:
                    return '', 500

                user_coupon['coupons'] = coupons

        return jsonify({'userCoupons': user_coupons})

    def put(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['user_coupons_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        amount = data['amount']
        user_id = data['userId']
        store_id = data['storeId']
        flag, coupons = self.db.find_by_condition(
            'coupons', {'storeId': store_id, 'pay': {'$lte': amount}})
        if not flag:
            return '', 500

        if not coupons:
            return jsonify({'id': user_id})

        coupon_id = coupons[0]['id']
        pay = coupons[0]['pay']
        for coupon in coupons:
            if coupon['pay'] > pay:
                coupon_id = coupon['id']

        flag, user_coupon = self.db.find_by_condition(
            'userCoupons', {'storeId': store_id, 'userId': user_id})
        if not flag:
            return '', 500

        if user_coupon:
            user_coupon_id = user_coupon[0]['id']
            flag, result = self.db.update('userCoupons', {
                'id': user_coupon_id}, {'$push': {'coupons': coupon_id}})
            if not flag:
                self.logger.error('update user coupon failed')
                return '', 500

            if not result:
                return self.error_msg(self.ERR['user_coupon_not_exist'])

            return jsonify(result)

        else:
            result = self.db.create('userCoupons', {'storeId': store_id,
                                                    'userId': user_id,
                                                    'coupons': [coupon_id]})
            if not result:
                self.logger.error('create user coupon failed')
                return '', 500

            return jsonify(result)


class UserCouponRemover(Base):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['user_coupon_remover_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        user_id = data['userId']
        store_id = data['storeId']
        coupon_id = data['couponId']
        flag, result = self.db.update('userCoupons', {
            'userId': user_id, 'storeId': store_id}, {
            '$pull': {'coupons': coupon_id}})
        if not flag:
            return '', 500

        if not result:
            return self.error_msg(self.ERR['user_coupon_not_exist'])

        return jsonify(result)
