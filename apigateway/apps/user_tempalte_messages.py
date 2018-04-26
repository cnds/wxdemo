import requests
from flask import request, jsonify

from .base import BaseHandler
from .json_validate import SCHEMA


class UserTemplateMessages(BaseHandler):

    def post(self, user_id):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['user_template_messages_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        data['userId'] = user_id
        api_resp = requests.post(
            '{0}/transactions/messages'.format(self.endpoint['transactions']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status
