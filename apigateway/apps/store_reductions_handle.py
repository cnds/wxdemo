import requests
from flask import request, jsonify
from .base import BaseHandler
from .json_validate import SCHEMA


class StoreReductionsHandler(BaseHandler):

    def get(self, store_id):
        api_resp = requests.get(
            '{0}/transactions/reductions'.format(self.endpoint['transactions']),
            params={'storeId': store_id})
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status

    def put(self, store_id):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['store_reductions_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        data['storeId'] = store_id
        api_resp = requests.put(
            '{0}/transactions/reductions'.format(self.endpoint['transactions']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status


class StoreReductionHandler(BaseHandler):

    def delete(self, store_id, reduction_id):
        api_resp = requests.delete(
            '{0}/transactions/reductions/{1}'.format(
                self.endpoint['transactions'], reduction_id),
            params={'storeId': store_id})
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status
