import requests
from flask import request, jsonify
from jybase.utils import create_md5_key
from config import config
from .base import BaseHandler


class StoreInfoHandler(BaseHandler):

    def get(self, user_id, code):
        flag, tag = self.authenticate(request, user_id, 
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        api_resp = requests.get(
            '{0}/accounts/store-info/{1}'.format(self.endpoint['accounts'],
                                                 code))
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            self.logger.error('request accounts server failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status
