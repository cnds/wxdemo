import requests
from flask import request, jsonify

from .json_validate import SCHEMA
from .base import Base


class UserPointsMall(Base):

    def get(self, user_id):
        params = request.args.to_dict()
        flag, tag = self.validate_dict_with_schema(
            params, SCHEMA['user_points_mall_get'])
        if not flag:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        params['userId'] = user_id
        flag, orders = self.db.find_by_condition('orders', params)
        if not flag:
            return '', 500

        store_id_list = list(set([order['storeId'] for order in orders]))
        result = list()
        for store_id in store_id_list:
            result_item = dict()
            flag, coupons = self.db.find_by_condition('coupons',
                                                      {'storeId': store_id})
            if not flag:
                return '', 500

            api_resp = requests.get(
                '{0}/accounts/stores/{1}'.format(self.endpoint['accounts'],
                                                 store_id))
            resp_status = api_resp.status_code
            if resp_status != 200:
                if resp_status == 400:
                    return jsonify(api_resp.json()), resp_status

                return '', 500

            store = api_resp.json()
            result_item.update({
                'storeName': store.get('storeName'),
                'address': store.get('address'),
                'coupons': coupons
            })

            result.append(result_item)

        return jsonify({'pointMall': result})

