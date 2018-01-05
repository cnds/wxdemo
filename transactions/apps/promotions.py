from flask import request, jsonify
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
                "coupon": {"pay": 0, "base": 0, "minus": 0},
                "storeId": params["storeId"]
            }

        return jsonify(promotions)

    def put(self):
        is_valid, data = self.get_params_from_request(request,
                                                      SCHEMA['promotions_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        store_id = data['storeId']
        flag, tag = self.db.update(
            'promotions', {'storeId': store_id}, {'$set': data}, True)
        if not flag:
            return '', 500

        if tag is None:
            return self.error_msg(self.ERR['not_found'])

        return jsonify({'result': tag}), 200


class Promotion(Base):

    def get(self, promotion_id):
        flag, promotion = self.db.find_by_id('promotions', promotion_id)
        if not flag:
            return '', 500

        if not promotion:
            return self.error_msg(self.ERR['promotion_not_exist'])

        return jsonify(promotion)
