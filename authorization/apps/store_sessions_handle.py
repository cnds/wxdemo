import requests
from flask import request, jsonify

from apps.base import BaseHandler
from apps.json_validate import SCHEMA


class StoreSessionsHandler(BaseHandler):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['store_sessions_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        api_resp = requests.post(
            '{0}/accounts/store-sessions'.format(self.endpoint['accounts']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            self.logger.error('request account server failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status
