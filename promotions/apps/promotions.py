from flask import request, jsonify
from apps.base import Base
from apps.json_validate import SCHEMA


class Promotions(Base):

    def get(self):
        params = request.args.to_dict()
        is_valid, tag = self.validate_dict_with_schema(params,
                                                       SCHEMA['promotions_get'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        flag, promotions = self.db.find_by_condition('promotions', params)
        if not flag:
            return '', 500

        if not promotions:
            promotions = {
                "discount": {"base": 0, "minus": 0},
                "coupon": {"base": 0, "minus": 0}
            }
            if params.get("storeId"):
                promotions.update({'storeId': params['storeId']})

        return jsonify({'promotions': promotions})

    def put(self):
        is_valid, data = self.get_params_from_request(request,
                                                      SCHEMA['promotions_put'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        store_id = data['storeId']
        flag, tag = self.db.update(
            'promotions', {'storeId': store_id}, data, True)
        if not flag:
            return '', 500

        if tag is None:
            return self.error_msg(self.ERR['not_found'])

        return jsonify({'result': tag}), 200
