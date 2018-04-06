import requests
from flask import request, jsonify

from .base import Base
from .json_validate import SCHEMA


class Points(Base):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['points_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        condition = self.get_data_with_keys(data, ('storeId', 'userId'))
        flag, point = self.db.find_by_condition('points', condition)
        if not flag:
            return '', 500

        if point:
            return self.error_msg(self.ERR['conflict_info_exist'])

        result = self.db.create('points', data)
        if not result:
            return '', 500

        return jsonify(result), 201

    def get(self):
        params = request.args.to_dict()
        flag, tag = self.validate_dict_with_schema(
            params, SCHEMA['points_get'])
        if not flag:
            return self.error_msg(self.ERR['invalid_query_params'])

        flag, points = self.db.find_by_condition('points', params)
        if not flag:
            return '', 500

        for point in points:
            store_id = point['storeId']
            api_resp = requests.get(
                '{0}/accounts/stores/{1}'.format(self.endpoint['accounts'],
                                                 store_id))
            resp_status = api_resp.status_code
            if resp_status != 200 and resp_status != 400:
                self.logger.error('request accounts service failed')
                return '', 500

            store = api_resp.json()
            point['storeName'] = store.get('storeName')
            point['address'] = store.get('address')

        return jsonify({'points': points}), 200


class PointsIncrease(Base):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['points_increase_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        point = data['point']
        condition = self.get_data_with_keys(data, ('storeId', 'userId'))
        flag, point_record = self.db.find_by_condition('points', condition)
        if not flag:
            return '', 500

        if point_record:
            point_id = point_record[0]['id']
            flag, result = self.db.update('points', {'id': point_id},
                                          {'$inc': {'point': point}})
            if not flag:
                return '', 500
        else:
            result = self.db.create('points', data)
            if not result:
                return '', 500

        return jsonify(result), 201


class PointsDecrease(Base):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['points_decrease_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        point = data['point']
        condition = self.get_data_with_keys(data, ('storeId', 'userId'))
        flag, point_record = self.db.find_by_condition('points', condition)
        if not flag:
            return '', 500

        if point_record:
            point_id = point_record[0]['id']
            point_from_db = point_record[0]['point']
            if point_from_db < point:
                return self.error_msg(self.ERR['insufficient_point'])

            flag, result = self.db.update('points', {'id': point_id},
                                          {'$inc': {'point': -point}})
            if not flag:
                return '', 500
        else:
            return self.error_msg(self.ERR['insufficient_point'])

        return jsonify(result), 201
