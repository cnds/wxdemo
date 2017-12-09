import requests
from flask import request, jsonify
from apps.base import BaseHandler
from apps.json_validate import SCHEMA


class PromotionsHandler(BaseHandler):

    def get(self, store_id):
        api_resp = requests.get(
            '{0}/promotions'.format(self.endpoint['promotions']),
            params={'storeId': store_id})
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            self.logger.error('request promotions server failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status

    def put(self, store_id):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['promotions_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        data['storeId'] = store_id
        api_resp = requests.put(
            '{0}/promotions'.format(self.endpoint['promotions']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            self.logger.error('request account server failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status


