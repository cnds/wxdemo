import requests
from flask import request, jsonify
from apps.base import Base
from apps.json_validate import SCHEMA


class Transactions(Base):

    def get(self):
        params = request.args.to_dict()
        flag, tag = self.str_to_int(params)
        if not flag:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        is_valid, tag = self.validate_dict_with_schema(
            params, SCHEMA['transactions_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        skip = params.pop('skip', 0)
        limit = params.pop('limit', 20)
        flag, transactions = self.db.find_by_condition(
            'transactions', params, skip, limit)
        if not flag:
            return '', 500

        user_id_list = set()
        store_id_list = set()
        for transaction in transactions:
            user_id_list.add(transaction['userId'])
            store_id_list.add(transaction['storeId'])

        api_resp = requests.get(
            '{0}/accounts/users'.format(self.endpoint['accounts']),
            params={'id': list(user_id_list)})
        resp_status = api_resp.status_code
        if resp_status != 200:
            if resp_status == 400:
                return self.error_msg(api_resp.json())

            return '', 500

        users = api_resp.json()['users']

        api_resp = requests.get(
            '{0}/accounts/stores/profile'.format(self.endpoint['accounts']),
            params={'storeId': list(store_id_list)})
        resp_status = api_resp.status_code
        if resp_status != 200:
            if resp_status == 400:
                return self.error_msg(api_resp.json())

            return '', 500

        stores = api_resp.json()['storeProfiles']
        result = list()
        for transaction in transactions:
            store_id = transaction['storeId']
            for store in stores:
                if store_id == store['storeId']:
                    transaction['storeName'] = store['storeName']

            user_id = transaction['userId']
            for user in users:
                if user_id == user['id']:
                    transaction['nickName'] = user['nickName']

            transaction_result = self.get_data_with_keys(transaction, (
                'storeName', 'nickName', 'address', 'amount', 'createdDate'))
            result.append(transaction_result)
        return jsonify({'transactions': result})

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
        params = request.args.to_dict()
        is_valid, tag = self.validate_dict_with_schema(
            params, SCHEMA['transaction_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        store_id = params.get('storeId')
        user_id = params.get('userId')
        flag, transaction = self.db.find_by_id('transactions', transaction_id)
        if not flag:
            return '', None

        if transaction is None:
            return self.error_msg(self.ERR['not_found'])

        if store_id:
            store_id_from_db = transaction.get('storeId')
            if store_id != store_id_from_db:
                return self.error_msg(self.ERR['permission_denied'])

        if user_id:
            user_id_from_db = transaction.get('userId')
            if user_id != user_id_from_db:
                return self.error_msg(self.ERR['permission_denied'])

        return jsonify(transaction), 200
