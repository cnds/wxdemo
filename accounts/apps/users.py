from flask import request, jsonify
from bson import ObjectId
from wxbase.utils import WXBizDataCrypt
from .base import Base
from .json_validate import SCHEMA
from config import config


class Users(Base):

    def get(self):

        # TODO: need to optimize the way of checking query params

        params = request.args.to_dict()
        is_valid, tag = self.validate_dict_with_schema(params,
                                                       SCHEMA['users_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        ids = params.pop('id', None)

        if ids:
            params['_id'] = {
                '$in': [ObjectId(i) for i in request.args.getlist('id')]}

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
        flag, data_from_wx = self.get_data_from_wx(code)
        if not flag:
            return '', 500

        if not data_from_wx:
            self.error_msg(self.ERR['invalid_wx_code'])

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


class UserRegisterStatus(Base):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['user_register_status_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        code = data['code']
        flag, data_from_wx = self.get_data_from_wx(code)
        if not flag:
            return '', 500

        if not data_from_wx:
            self.error_msg(self.ERR['invalid_wx_code'])

        open_id = data_from_wx['openid']
        flag, user = self.db.find_by_condition('users', {'openId': open_id})
        if not flag:
            return '', 500

        if not user:
            return self.error_msg(self.ERR['user_not_exist'])

        return jsonify({'openId': open_id}), 201
