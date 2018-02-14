import requests
from flask import request, jsonify
from .base import BaseHandler
from .json_validate import SCHEMA


class StoreDiscountsHandler(BaseHandler):

    def get(self, store_id):
        api_resp = requests.get(
            '{0}/transactions/discounts'.format(
                self.endpoint['transactions']),
            params={'storeId': store_id})
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status

    def post(self, store_id):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['store_discounts_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        data['storeId'] = store_id
        api_resp = requests.post(
            '{0}/transactions/discounts'.format(
                self.endpoint['transactions']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status


class StoreDiscountHandler(BaseHandler):

    def get(self, store_id, discount_id):
        api_resp = requests.get(
            '{0}/transactions/discounts/{1}'.format(
                self.endpoint['transactions'], discount_id),
            params={'storeId': store_id})
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status

    def put(self, store_id, discount_id):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['store_discount_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        data['storeId'] = store_id
        api_resp = requests.put(
            '{0}/transactions/discounts/{1}'.format(
                self.endpoint['transactions'], discount_id),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status

    def delete(self, store_id, discount_id):
        api_resp = requests.delete(
            '{0}/transactions/discounts/{1}'.format(
                self.endpoint['transactions'], discount_id),
            params={'storeId': store_id})
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status
