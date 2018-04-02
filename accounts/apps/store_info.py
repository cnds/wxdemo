from flask import jsonify

from .base import Base


class StoreInfo(Base):

    def get(self, code):
        flag, qr_info = self.db.find_by_condition('QRCode', {'code': code})
        if not flag:
            return '', 500

        if not qr_info:
            return self.error_msg(self.ERR['qr_code_not_exist'])

        store_id = qr_info[0]['storeId']
        wechat_info = qr_info[0].get('wechatInfo')
        flag, store = self.db.find_by_id('stores', store_id)
        if not flag:
            return '', 500

        if not store:
            return self.error_msg(self.ERR['store_not_exist'])

        store['code'] = code
        if wechat_info:
            store['wechatInfo'] = wechat_info
        return jsonify(store), 200
