from flask import request, jsonify
from apps.base import Base
from apps.json_validate import SCHEMA


class Transactions(Base):

    def get(self):
        params = request.args.to_dict()
        is_valid, tag = self.validate_dict_with_schema(
            params, SCHEMA['transactions_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        flag, transactions = self.db.find_by_condition('transactions', params)
        if not flag:
            return '', 500

        return jsonify({'transactions': transactions})

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['transactions_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        result = self.db.create('transactions', data)
        if not result:
            return '', 500

        return jsonify(result), 200


class Transaction(Base):

    def get(self, transaction_id):
        flag, transaction = self.db.find_by_id('transactions', transaction_id)
        if not flag:
            return '', None

        if transaction is None:
            return self.error_msg(self.ERR['not_found'])

        return jsonify(transaction), 200
