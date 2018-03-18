import requests
from flask import request, jsonify
from config import config
from .base import BaseHandler
from .json_validate import SCHEMA
from jybase.utils import create_md5_key


class StoreCouponsHandler(BaseHandler):

    def get(self, store_id):
        flag, tag = self.authenticate(request, store_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        params = request.args.to_dict()
        # is_valid, tag = self.validate_dict_with_schema(
        #     params, SCHEMA['store_coupons_get'])
        # if not is_valid:
        #     return self.error_msg(self.ERR['invalid_query_params'], tag)

        params['storeId'] = store_id
        api_resp = requests.get(
            '{0}/transactions/coupons'.format(self.endpoint['transactions']),
            params=params)
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status

    def post(self, store_id):
        flag, tag = self.authenticate(request, store_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        is_valid, data = self.get_params_from_request(
            request, SCHEMA['store_coupons_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        data['storeId'] = store_id
        api_resp = requests.post(
            '{0}/transactions/coupons'.format(self.endpoint['transactions']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status


class StoreCouponHandler(BaseHandler):

    def get(self, store_id, coupon_id):
        flag, tag = self.authenticate(request, store_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        api_resp = requests.get(
            '{0}/transactions/coupons/{1}'.format(
                self.endpoint['transactions'], coupon_id),
            params={'storeId': store_id})
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status

    def put(self, store_id, coupon_id):
        flag, tag = self.authenticate(request, store_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        is_valid, data = self.get_params_from_request(
            request, SCHEMA['store_coupon_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        data['storeId'] = store_id
        api_resp = requests.put(
            '{0}/transactions/coupons/{1}'.format(
                self.endpoint['transactions'], coupon_id),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status

    def delete(self, store_id, coupon_id):
        flag, tag = self.authenticate(request, store_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        api_resp = requests.delete(
            '{0}/transactions/coupons/{1}'.format(
                self.endpoint['transactions'], coupon_id),
            params={'storeId': store_id})
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status
