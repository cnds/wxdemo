import requests
from flask import request, jsonify
from jybase.utils import create_md5_key
from config import config
from .base import BaseHandler
from .json_validate import SCHEMA


class UserPaymentDetailHandler(BaseHandler):

    def post(self, user_id):
        flag, tag = self.authenticate(request, user_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        is_valid, data = self.get_params_from_request(
            request, SCHEMA['user_payment_detail_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        data['userId'] = user_id
        api_resp = requests.post(
            '{0}/transactions/payment-detail'.format(
                self.endpoint['transactions']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            self.logger.error('request transactions server failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status
