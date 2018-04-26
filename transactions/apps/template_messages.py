import requests
from flask import request, jsonify

from .base import Base
from .json_validate import SCHEMA
from config import config


class TemplateMessages(Base):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['template_messages_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        order_id = data['orderId']
        form_id = data['formId']
        open_id = data['openId']
        user_id = data['userId']

        flag, order = self.db.find_by_id('orders', order_id)
        if not flag:
            return '', 500

        if order is None:
            return self.error_msg(self.ERR['order_not_exist'])

        user_id_from_order = order['userId']
        if user_id != user_id_from_order:
            return self.error_msg(self.ERR['permission_denied'])

        # get nickname
        api_resp = requests.get(
            '{0}/accounts/users/{1}'.format(self.endpoint['accounts'], user_id))
        resp_status = api_resp.status_code
        if resp_status != 200:
            if resp_status == 400:
                return jsonify(api_resp.json()), 400

            return '', 500

        user = api_resp.json()
        nickname = user['nickName']

        template_data = {
            'keyword1': {'DATA': nickname},
            'keyword2': {'DATA': str(order['createdDate'])},
            'keyword3': {'DATA': order['amount']}
        }

        app_id = config['wechat']['user']['appId']
        secret = config['wechat']['user']['appSecret']
        access_token = self.get_access_token(app_id, secret)
        # get access token

        # send template message

        template_id = config['template']['applyPoints']
        result = self.send_template_message(access_token, open_id,
                                            template_id, '/transactions',
                                            form_id, template_data)
        if not result:
            return self.error_msg(self.ERR['send_template_message_failed'])

        return jsonify({'id': open_id})

