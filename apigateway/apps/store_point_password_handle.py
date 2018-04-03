import requests
from flask import jsonify, request

from .base import BaseHandler
from .json_validate import SCHEMA


class StorePointPassword(BaseHandler):

    def get(self, store_id):
        api_resp = requests.get(
            '{0}/accounts/stores/{1}/point-password'.format(
                self.endpoint['accounts'], store_id))
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            self.logger.error('request account service failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status

    def post(self, store_id):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['store_point_password_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        api_resp = requests.post(
            '{0}/accounts/stores/{1}/point-password'.format(
                self.endpoint['accounts'], store_id),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            self.logger.error('request accounts service failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status

    def put(self, store_id):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['store_point_password_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        api_resp = requests.put(
            '{0}/accounts/stores/{1}/point-password'.format(
                self.endpoint['accounts'], store_id),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            self.logger.error('request accounts service failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status
