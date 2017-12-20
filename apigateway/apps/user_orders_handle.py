import requests
from flask import request, jsonify
from wxbase.utils import create_md5_key
from .base import BaseHandler
from .json_validate import SCHEMA
from config import config


class UserOrdersHandler(BaseHandler):

    def get(self, user_id):
        flag, tag = self.authenticate(request, user_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        params = request.args.to_dict()
        flag, tag = self.str_to_int(params)
        if not flag:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        is_valid, tag = self.validate_dict_with_schema(
            params, SCHEMA['user_orders_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        params['userId'] = user_id
        api_resp = requests.get(
            '{0}/transactions/orders'.format(self.endpoint['transactions']),
            params=params)
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            self.logger.error('request transactions server failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status


class UserOrderHandler(BaseHandler):

    def get(self, user_id, order_id):
        flag, tag = self.authenticate(request, user_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        params = {'userId': user_id}
        api_resp = requests.get(
            '{0}/transactions/orders/{1}'.format(
                self.endpoint['transactions'], order_id),
            params=params)
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            self.logger.error('request transactions server failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status