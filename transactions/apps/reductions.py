from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class Reductions(Base):

    def get(self):
        params = request.args.to_dict()
        is_valid, tag = self.validate_dict_with_schema(params,
                                                       SCHEMA['reductions_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        flag, reductions = self.db.find_by_condition('reductions', params)
        if not flag:
            return '', 500

        return jsonify({'reductions': reductions})

    def put(self):
        is_valid, data = self.get_params_from_request(request,
                                                      SCHEMA['reductions_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        store_id = data['storeId']
        reduction = data['percent']

        # need to set storeId index in mongodb
        # prevent inserting duplicate data
        # see mongodb docs
        flag, result = self.db.update(
            'reductions',
            {'storeId': store_id},
            {'$set': {'percent': reduction}},
            upsert=True)

        if not flag:
            return '', 500

        return jsonify(result)


class Reduction(Base):

    def delete(self, reduction_id):
        params = request.args.to_dict()
        store_id = params.get('storeId')
        flag, reduction = self.db.find_by_id('reductions', reduction_id)
        if not flag:
            return '', 500

        if not reduction:
            return self.error_msg(self.ERR['reduction_not_exist'])

        if store_id:
            store_id_from_db = reduction['storeId']
            if store_id != store_id_from_db:
                return self.error_msg(self.ERR['permission_denied'])

        flag, result = self.db.remove('reductions', reduction_id)
        if not flag:
            return '', 500

        if result is None:
            return self.error_msg(self.ERR['reduction_has_been_removed'])

        return jsonify(result)
