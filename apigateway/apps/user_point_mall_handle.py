import requests
from flask import request, jsonify

from .base import BaseHandler
from .json_validate import SCHEMA


class UserPointMallHandler(BaseHandler):

    def get(self, user_id):
        params = request.args.to_dict()
        flag, tag = self.validate_dict_with_schema(
            params, SCHEMA['user_point_mall_get'])
        if not flag:
            return self.error_msg(self.ERR['invalid_query_params'])

        api_resp = requests.get(
            '{0}/transactions/{1}/point-mall'.format(
                self.endpoint['transactions'], user_id),
            params=params)
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            self.logger.error('request transaction service failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status