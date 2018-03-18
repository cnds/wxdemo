import requests
from flask import request, jsonify
from .base import BaseHandler
from .json_validate import SCHEMA
from jybase.utils import create_md5_key
from config import config


class StoreHandler(BaseHandler):

    def get(self, store_id):
        flag, tag = self.authenticate(request, store_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        api_resp = requests.get(
            '{0}/accounts/stores/{1}'.format(self.endpoint['accounts'],
                                             store_id))
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            self.logger.error('request accounts server failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status

    def put(self, store_id):
        flag, tag = self.authenticate(request, store_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        is_valid, data = self.get_params_from_request(
            request, SCHEMA['store_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        api_resp = requests.put(
            '{0}/accounts/stores/{1}'.format(self.endpoint['accounts'],
                                             store_id),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            self.logger.error('request accounts server failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status


class StoreBindQRCodeHandler(BaseHandler):

    def post(self, store_id):
        flag, tag = self.authenticate(request, store_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        is_valid, data = self.get_params_from_request(
            request, SCHEMA['store_bind_qr_code_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        data['storeId'] = store_id
        api_resp = requests.post(
            '{0}/accounts/qr-code/bind-store'.format(
                self.endpoint['accounts']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            self.logger.error('request accounts server failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status


class StoreBindPaymentInfoHandler(BaseHandler):

    def post(self, store_id):
        flag, tag = self.authenticate(request, store_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        is_valid, data =self.get_params_from_request(
            request, SCHEMA['store_bind_payment_info_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        data['storeId'] = store_id
        api_resp = requests.post(
            '{0}/accounts/qr-code/bind-payment-info'.format(
                self.endpoint['accounts']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            self.logger.error('request accounts server failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status
