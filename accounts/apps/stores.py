from flask import jsonify, request

from wxbase.utils import create_md5_key, create_hash_key
from accounts.apps.base import Base
from accounts.apps.json_validate import SCHEMA



class Stores(Base):

    def get(self):
        params = request.args.to_dict()
        is_valid, tag = self.validate_dict_with_schema(params,
                                                       SCHEMA['stores_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], tag)

        flag, stores = self.db.find_by_condition('stores', params)
        if not flag:
            return '', 500

        return jsonify({'stores': stores})

    def post(self):

        # TODO: sms validate

        is_valid, data = self.get_params_from_request(request,
                                                     SCHEMA['stores_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        mobile = data['mobile']
        password = data['password']
        flag, store_from_db = self.db.find_by_condition('stores',
                                                        {'mobile': mobile})
        if not flag:
            return '', 500

        if store_from_db:
            account_status = store_from_db[0]['status']
            if account_status == 'processing':
                store_id = store_from_db[0]['id']
            else:
                return self.error_msg(self.ERR['conflict_user_exist'])

        else:
            data['status'] = 'processing'
            store = self.db.create('stores', data)
            if not store:
                return '', 500

            store_id = store['id']

        salt = create_md5_key((store_id))
        password = create_hash_key(password, salt)
        flag, result = self.db.update(
            'stores', {'id': store_id},
            {'$set': {'password': password, 'status': 'done'}})
        if not flag:
            return '', 500

        if not result:
            return self.error_msg(self.ERR['not_found'])

        return jsonify({'id': store_id}), 201


class Store(Base):

    def get(self, store_id):
        return '', 405

    def put(self, store_id):
        return '', 405

    def delete(self, store_id):
        return '', 405
