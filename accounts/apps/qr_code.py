from flask import request, jsonify
from .base import Base
from .json_validate import SCHEMA


class QRCodeBindStore(Base):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['qr_code_bind_store_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        store_id = data['storeId']
        qr_code = data['QRCode']
        flag, code = self.db.find_by_condition('QRCode', {'code': qr_code})
        if not flag:
            return '', 500

        if code:
            store_id_from_db = code[0].get('storeId')
            if store_id_from_db:
                return self.error_msg(self.ERR['qr_code_already_been_bound'])
        else:
            return self.error_msg(self.ERR['qr_code_not_exist'])

        flag, store = self.db.find_by_id('stores', store_id)
        if not flag:
            return '', 500

        if not store:
            return self.error_msg(self.ERR['store_not_exist'])

        flag, tag = self.db.update('QRCode', {'code': qr_code},
                                   {'$set': {'storeId': store_id}})
        if not flag:
            return '', 500

        return jsonify(tag), 200