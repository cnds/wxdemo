from flask import request, jsonify
from jybase.utils import create_md5_key
from .base import Base
from .json_validate import SCHEMA
from config import config


class UserSessions(Base):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['user_sessions_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        open_id = data['openId']
        flag, user = self.db.find_by_condition('users', {'openId': open_id})
        if not flag:
            return '', 500

        if len(user) == 0:
            return self.error_msg(self.ERR['user_not_found'])

        user = user[0]
        user_id = user['id']
        salt = create_md5_key(config['secret'])
        token = self.create_jwt({'accountId': user_id}, salt)
        return jsonify({'id': user_id, 'token': token.decode()}), 201
