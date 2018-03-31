import requests
from flask import request, jsonify
from .base import BaseHandler
from .json_validate import SCHEMA


class UserRegisterStatus(BaseHandler):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['user_register_status_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        api_resp = requests.post(
            '{0}/accounts/users/register-status'.format(self.endpoint['accounts']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status


class Users(BaseHandler):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['users_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        api_resp = requests.post(
            '{0}/accounts/users'.format(self.endpoint['accounts']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            return '', 500

        return jsonify(api_resp.json()), resp_status
