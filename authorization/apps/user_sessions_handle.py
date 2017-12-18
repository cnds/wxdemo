import requests
from flask import request, jsonify

from .base import BaseHandler
from .json_validate import SCHEMA


class UserSessionsHandler(BaseHandler):

    def post(self):
        remote_ip = request.environ['REMOTE_ADDR']
        if self.redis.check_if_block(remote_ip):
            return self.error_msg(self.ERR['attempt_too_many_times'])

        is_valid, data = self.get_params_from_request(
            request, SCHEMA['user_sessions_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        api_resp = requests.post(
            '{0}/accounts/user-sessions'.format(self.endpoint['accounts']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201:
            if resp_status == 400:
                self.redis.set_ip_block(remote_ip)
                return jsonify(api_resp.json()), 400

            self.logger.error('request account server failed')
            return '', 500

        return jsonify(api_resp.json()), 201
