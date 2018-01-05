from flask import request, jsonify
from pymongo import UpdateOne
from .base import Base
from .json_validate import SCHEMA


class Promotions(Base):

    def get(self):
        params = request.args.to_dict()
        is_valid, tag = self.validate_dict_with_schema(
            params, SCHEMA['promotions_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        flag, promotions = self.db.find_by_condition('promotions', params)
        if not flag:
            return '', 500

        if promotions:
            promotions = promotions[0]
        else:
            promotions = {
                "reduction": 100,
                "discount": {"base": 0, "minus": 0},
                "coupons": [{"pay": 0, "base": 0, "minus": 0}],
                "storeId": params["storeId"]
            }

        return jsonify(promotions)

    def put(self):
        is_valid, data = self.get_params_from_request(request,
                                                      SCHEMA['promotions_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        store_id = data['storeId']
        reduction = data.get('reduction')
        discount = data.get('discount')
        coupons = data.get('coupons')
        data_to_update = list()
        if reduction:
            data_to_update.append(
                UpdateOne(
                    {'storeId': store_id, 'reduction': {'$exists': True}},
                    {'$set': {'reduction': reduction}}, upsert=True))

        if discount:
            data_to_update.append(
                UpdateOne(
                    {'storeId': store_id, 'discount': {'$exists': True}},
                    {'$set': {'discount': discount}}, upsert=True))
        if coupons:
            for coupon in coupons:
                data_to_update.append(
                    UpdateOne(
                        {'storeId': store_id, 'coupon': coupon},
                        {'$set': {'coupon': coupon}}, upsert=True))

        flag, result = self.db.bulk_update('promotions', data_to_update)
        if not flag:
            return '', 500

        if result is None:
            return self.error_msg(self.ERR['db_bulk_update_error'])

        return jsonify({'result': result}), 200


class Promotion(Base):

    def get(self, promotion_id):
        flag, promotion = self.db.find_by_id('promotions', promotion_id)
        if not flag:
            return '', 500

        if not promotion:
            return self.error_msg(self.ERR['promotion_not_exist'])

        return jsonify(promotion)
