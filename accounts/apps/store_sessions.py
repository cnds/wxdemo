from flask import request, jsonify

from .base import Base
from .json_validate import SCHEMA
from wxbase.utils import validate_hash_key, create_md5_key
from config import config


class StoreSessions(Base):

    def post(self):

        # TODO: add sms login

        is_valid, data = self.get_params_from_request(
            request, SCHEMA['store_sessions_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        mobile = data['mobile']
        password = data['password']
        flag, store = self.db.find_by_condition('stores', {'mobile': mobile})
        if not flag:
            return '', 500

        if len(store) == 0:
            return self.error_msg(self.ERR['user_not_found'])

        store = store[0]
        store_id = store['id']
        password_from_db = store['password']
        salt = create_md5_key(store_id + config['secret'])
        if not validate_hash_key(password, password_from_db, salt):
            return self.error_msg(self.ERR['password_verification_failed'])

        token = self.create_jwt({'accountId': store_id}, salt)
        result = self.get_data_with_keys(
                store, ('mobile', 'id', 'address', 'storeName'),
                {'token': token.decode()})
        return jsonify(result), 201
