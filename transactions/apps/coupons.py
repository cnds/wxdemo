from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class Coupons(Base):

    def get(self):
        params = request.args.to_dict()
        flag, tag = self.validate_dict_with_schema(params,
                                                   SCHEMA['coupons_get'])
        if not flag:
            return self.error_msg(self.ERR['invalid_query_params'], tag)

        flag, coupons = self.db.find_by_condition('coupons', params)
        if not flag:
            return '', 500

        return jsonify({'coupons': coupons})
