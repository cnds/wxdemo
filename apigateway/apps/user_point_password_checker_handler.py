import requests
from flask import request, jsonify
from jybase.utils import create_md5_key

from .base import BaseHandler
from .json_validate import SCHEMA

from config import config


class PointPasswordCheckerHandler(BaseHandler):

    def post(self, user_id):
        flag, tag = self.authenticate(request, user_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        is_valid, data = self.get_params_from_request(
            request, SCHEMA['point_password_checker_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        store_id = data.pop('storeId')
        api_resp = requests.post(
            '{0}/accounts/stores/{1}/point-password/checker'.format(
                self.endpoint['accounts'], store_id),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            self.logger.error('request accounts service failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status
