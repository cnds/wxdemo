from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class StoreProfile(Base):

    def get(self, store_id):
        flag, store = self.db.find_by_id('stores', store_id)
        if not flag:
            return '', 500

        if store is None:
            return self.error_msg(self.ERR['user_not_found'])

        flag, profile = self.db.find_by_condition('storeProfile',
                                                  {'storeId': store_id})
        if not flag:
            return '', 500

        if profile:
            store.update(profile[0])

        result = self.get_data_with_keys(store, ('mobile', 'address', 'name'))

        return jsonify(result), 200

    def put(self, store_id):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['store_profile_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        flag, store = self.db.find_by_id('stores', store_id)
        if not flag:
            return self.error_msg(self.ERR['user_not_found'])

        flag, profile = self.db.update('storeProfile', {'storeId': store_id},
                                       {'$set': data}, True)
        if not flag:
            return '', 500

        if not profile:
            return self.error_msg(self.ERR['operation_failed'])

        return jsonify(profile), 200


class StoreProfiles(Base):

    def get(self):
        params = request.args.to_dict()
        is_valid, tag = self.validate_dict_with_schema(
            params, SCHEMA['store_profiles_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        store_id = params.get('storeId')
        condition = {'storeId': store_id} if store_id else dict()
        flag, profiles = self.db.find_by_condition('storeProfile', condition)
        if not flag:
            return '', 500

        condition = {'id': store_id} if store_id else dict()
        flag, stores = self.db.find_by_condition('stores', condition)
        if not flag:
            return '', 500

        result = list()
        for profile in profiles:
            for store in stores:
                if store['id'] == profile['storeId']:
                    store.pop('id')
                    profile.update(store)
                    result.append(self.get_data_with_keys(
                        profile, ('mobile', 'address', 'name')))

        return jsonify({'storeProfiles': result}), 200
