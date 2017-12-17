import requests
from flask import request, jsonify
from wxbase.utils import WXBizDataCrypt
from .base import Base
from .json_validate import SCHEMA
from config import config


class Users(Base):

    def get(self):
        params = request.args.to_dict()
        is_valid, tag = self.validate_dict_with_schema(params,
                                                       SCHEMA['users_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        flag, users = self.db.find_by_condition('users', params)
        if not flag:
            return '', 500

        return jsonify({'users': users}), 200

    def post(self):
        is_valid, data = self.get_params_from_request(request,
                                                      SCHEMA['users_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        code = data['code']
        iv = data['iv']
        encrypted_data = data['encryptedData']
        query_params = {
            'appid': config['wechat']['appId'],
            'secret': config['wechat']['appSecret'],
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        api_resp = requests.get(
            'https://api.weixin.qq.com/sns/jscode2session',
            params=query_params)
        resp_status = api_resp.status_code
        if resp_status != 200:
            self.logger('request wechat server failed')
            return '', 500

        data_from_wx = api_resp.json()
        open_id = data_from_wx['openid']
        session_key = data_from_wx['session_key']

        flag, user = self.db.find_by_condition('users', {'oepnId': open_id})
        if not flag:
            self.logger.error('get users from db failed')
            return '', 500

        if user:
            return self.error_msg(self.ERR['conflict_user_exist'])

        pc = WXBizDataCrypt(config['wechat']['appId'], session_key)
        decrypted_data = pc.decrypt(encrypted_data, iv)
        result = self.db.create('users', decrypted_data)
        if not result:
            self.logger.error('create user failed')
            return '', 500

        return jsonify(result), 201
