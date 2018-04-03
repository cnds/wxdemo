from flask import request, jsonify

from .base import Base
from .json_validate import SCHEMA
from jybase.utils import create_md5_key, create_hash_key


class PointPassword(Base):

    def post(self, store_id):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['point_password_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        password = data['pointPassword']

        flag, store = self.db.find_by_condition('pointPassword',
                                                {'storeId': store_id})
        if not flag:
            return '', 500

        if store:
            point_password = store[0].get('pointPassword')
            if point_password:
                return self.error_msg(self.ERR['password_been_set'])

        salt = create_md5_key(store_id)
        hashed_password = create_hash_key(password, salt)
        data_to_insert = {
            'storeId': store_id,
            'pointPassword': hashed_password,
        }
        result = self.db.create('pointPassword', data_to_insert)
        if not result:
            return '', 500

        return jsonify(result), 201

    def get(self, store_id):
        flag, store = self.db.find_by_condition('pointPassword',
                                                {'storeId': store_id})
        if not flag:
            return '', 500

        if store:
            result = store[0]
        else:
            result = dict()

        return jsonify(result), 200

    def put(self, store_id):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['point_password_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        password = data['pointPassword']
        salt = create_md5_key(store_id)
        hashed_password = create_hash_key(password, salt)
        data_to_update = {
            'pointPassword': hashed_password
        }
        flag, result = self.db.update('pointPassword', {'storeId': store_id},
                                {'$set': data_to_update})
        if not flag:
            return '', 500

        return jsonify(result), 200


