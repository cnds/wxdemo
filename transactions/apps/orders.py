import requests
from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class Orders(Base):

    def get(self):
        params = request.args.to_dict()
        flag, tag = self.str_to_int(params)
        if not flag:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        is_valid, tag = self.validate_dict_with_schema(
            params, SCHEMA['orders_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        page = params.pop('page', 1)
        limit = params.pop('limit', 20)
        flag, orders = self.db.find_by_condition(
            'orders', params, page, limit)
        if not flag:
            return '', 500

        user_id_list = set()
        store_id_list = set()
        for order in orders:
            user_id_list.add(order['userId'])
            store_id_list.add(order['storeId'])

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
            '{0}/accounts/stores'.format(self.endpoint['accounts']),
            params={'id': list(store_id_list)})
        resp_status = api_resp.status_code
        if resp_status != 200:
            if resp_status == 400:
                return self.error_msg(api_resp.json())

            return '', 500

        stores = api_resp.json()['stores']
        result = list()
        for order in orders:
            store_id = order['storeId']
            for store in stores:
                if store_id == store['id']:
                    order['storeName'] = store['storeName']

            user_id = order['userId']
            for user in users:
                if user_id == user['id']:
                    order['nickName'] = user['nickName']

            transaction_result = self.get_data_with_keys(order, (
                'storeName', 'nickName', 'address', 'amount', 'createdDate'))
            result.append(transaction_result)
        return jsonify({'orders': result})

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['orders_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        result = self.db.create('orders', data)
        if not result:
            return '', 500

        return jsonify(result), 200


class Order(Base):

    def get(self, order_id):
        params = request.args.to_dict()
        is_valid, tag = self.validate_dict_with_schema(
            params, SCHEMA['order_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        store_id = params.get('storeId')
        user_id = params.get('userId')
        flag, order = self.db.find_by_id('orders', order_id)
        if not flag:
            return '', None

        if order is None:
            return self.error_msg(self.ERR['not_found'])

        if store_id:
            store_id_from_db = order.get('storeId')
            if store_id != store_id_from_db:
                return self.error_msg(self.ERR['permission_denied'])

        if user_id:
            user_id_from_db = order.get('userId')
            if user_id != user_id_from_db:
                return self.error_msg(self.ERR['permission_denied'])

        return jsonify(order), 200
