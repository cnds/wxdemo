import requests
from flask import request, jsonify

from .base import BaseHandler
from wxbase.utils import create_md5_key
from config import config


class QRCodes(BaseHandler):

    def get(self, store_id):
        flag, tag = self.authenticate(request, store_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        api_resp = requests.get(
            '{0}/accounts/qr-code'.format(self.endpoint['accounts']),
            params={'storeId': store_id})
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            self.logger.error('request accounts service failed')
            return '', 500

        qr_code = api_resp.json()['QRCodes']
        if qr_code:
            result = qr_code[0]
        else:
            result = dict()
        return jsonify(result), resp_status
