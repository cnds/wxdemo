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
        flag, result = self.db.remove('reductions', reduction_id)
        if not flag:
            return '', 500

        if result is None:
            return self.error_msg(self.ERR['reduction_has_been_removed'])

        return jsonify(result)
