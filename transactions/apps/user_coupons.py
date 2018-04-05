import requests

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
                    "coupons": {}
                },
                {
                    "userId": aaa,
                    "storeId": bbb,
                    "coupons": {}
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
            for user_coupon in user_coupons:
                from bson import ObjectId
                coupon_id_list = [ObjectId(coupon_id) for coupon_id
                                  in user_coupon['coupons'].keys()]
                flag, coupons = self.db.find_by_condition(
                    'coupons', {'_id': {'$in': coupon_id_list}})
                if not flag:
                    return '', 500

                for coupon in coupons:
                    coupon_num = user_coupon['coupons'].get(coupon['id'])
                    coupon['number'] = coupon_num

                user_coupon['coupons'] = coupons

                store_id = user_coupon['storeId']
                api_resp = requests.get(
                    '{0}/accounts/stores/{1}'.format(
                        self.endpoint['accounts'], store_id))
                resp_status = api_resp.status_code
                if resp_status != 200:
                    if resp_status == 400:
                        return self.error_msg(api_resp.json())

                    return '', 500

                store = api_resp.json()
                user_coupon['storeName'] = store['storeName']
                user_coupon['address'] = store['address']

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
                'id': user_coupon_id}, {'$inc': {'coupons.' + coupon_id: 1}})
            if not flag:
                self.logger.error('update user coupon failed')
                return '', 500

            if not result:
                return self.error_msg(self.ERR['user_coupon_not_exist'])

            return jsonify(result)

        else:
            result = self.db.create('userCoupons', {'storeId': store_id,
                                                    'userId': user_id,
                                                    'coupons': {coupon_id: 1}})
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
        flag, user_coupon = self.db.find_by_condition(
            'userCoupons', {'userId': user_id, 'storeId': store_id,
                            'coupons.' + coupon_id: {'$exists': True}})
        if not flag:
            return '', 500
        
        if not user_coupon:
            return self.error_msg(self.ERR['user_coupon_not_exist'])

        user_coupon_id = user_coupon[0]['id']
        coupon_num = user_coupon[0]['coupons'][coupon_id]
        if coupon_num < 1:
            return self.error_msg(self.ERR['user_coupon_not_exist'])

        elif coupon_num == 1:
            flag, result = self.db.update('userCoupons', {
                'id': user_coupon_id}, {'$unset': {'coupons.' + coupon_id: 1}})
            if not flag:
                return '', 500

            return jsonify(result), 201

        else:
            flag, result = self.db.update('userCoupons', {
                'id': user_coupon_id}, {'$inc': {'coupons.' + coupon_id: -1}})
            if not flag:
                return '', 500
            
            return jsonify(result), 201
