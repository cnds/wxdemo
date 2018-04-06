from flask import jsonify

from .base import Base


class StoreInfo(Base):

    def get(self, code):
        flag, qr_info = self.db.find_by_condition('QRCode', {'code': code})
        if not flag:
            return '', 500

        if not qr_info:
            return self.error_msg(self.ERR['qr_code_not_exist'])

        store_id = qr_info[0].get('storeId')
        if not store_id:
            return self.error_msg(self.ERR['code_with_no_store'])

        flag, store = self.db.find_by_id('stores', store_id)
        if not flag:
            return '', 500

        if not store:
            return self.error_msg(self.ERR['store_not_exist'])

        store['code'] = code
        return jsonify(store), 200
