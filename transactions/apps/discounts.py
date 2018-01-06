from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class Discounts(Base):

    def get(self):
        params = request.args.to_dict()
        is_valid, tag = self.validate_dict_with_schema(params,
                                                       SCHEMA['discounts_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        flag, discounts = self.db.find_by_condition('discounts', params)
        if not flag:
            return '', 500

        return jsonify({'discounts': discounts})

    def post(self):
        is_valid, data = self.get_params_from_request(request,
                                                      SCHEMA['discounts_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        store_id = data['storeId']
        discount_base = data['base']
        flag, discount = self.db.find_by_condition(
            'discounts', {'storeId': store_id, 'base': discount_base})
        if not flag:
            return '', 500

        if discount:
            return self.error_msg(self.ERR['conflict_discount'])

        result = self.db.create('discounts', data)
        if not result:
            return '', 500

        return jsonify(result)


class Discount(Base):

    def get(self, discount_id):
        flag, discount = self.db.find_by_id('discounts', discount_id)
        if not flag:
            return '', 500

        if not discount:
            return self.error_msg(self.ERR['discount_not_exist'])

        return jsonify(discount)

    def put(self, discount_id):
        is_valid, data = self.get_params_from_request(request,
                                                      SCHEMA['discount_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        flag, result = self.db.update('discounts', {'id': discount_id},
                                      {'$set': data})
        if not flag:
            return '', 500

        return jsonify(result)

    def delete(self, discount_id):
        flag, result = self.db.remove('discounts', discount_id)
        if not flag:
            return '', 500

        if result is None:
            return self.error_msg(self.ERR['discount_has_been_removed'])

        return jsonify(result)
