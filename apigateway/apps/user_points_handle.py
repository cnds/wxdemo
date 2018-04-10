import requests
from flask import request, jsonify

from .base import BaseHandler
from .json_validate import SCHEMA

from jybase.utils import create_md5_key
from config import config


class UserPointsHandler(BaseHandler):

    def get(self, user_id):
        flag, tag = self.authenticate(request, user_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        params = request.args.to_dict()
        flag, tag = self.validate_dict_with_schema(
            params, SCHEMA['user_points_get'])
        if not flag:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        params['userId'] = user_id
        api_resp = requests.get(
            '{0}/transactions/points'.format(self.endpoint['transactions']),
            params=params)
        resp_status = api_resp.status_code
        if resp_status != 200 and resp_status != 400:
            self.logger.error('request transaction service failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status


class IncreaseUserPointsHandler(BaseHandler):

    def post(self, user_id):
        flag, tag = self.authenticate(request, user_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        is_valid, data = self.get_params_from_request(
            request, SCHEMA['user_points_increase_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        data['userId'] = user_id
        api_resp = requests.post(
            '{0}/transactions/points/increase'.format(self.endpoint['transactions']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            self.logger.error('request transaction service failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status


class DecreaseUserPointsHandler(BaseHandler):

    def post(self, user_id):
        flag, tag = self.authenticate(request, user_id,
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)

        is_valid, data = self.get_params_from_request(
            request, SCHEMA['user_points_decrease_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        data['userId'] = user_id
        api_resp = requests.post(
            '{0}/transactions/points/decrease'.format(self.endpoint['transactions']),
            json=data)
        resp_status = api_resp.status_code
        if resp_status != 201 and resp_status != 400:
            self.logger.error('request transaction service failed')
            return '', 500

        return jsonify(api_resp.json()), resp_status

