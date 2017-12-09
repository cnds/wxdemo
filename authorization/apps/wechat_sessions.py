import requests

from flask import request
from wxbase.utils import create_jwt

from apps.base import BaseHandler
from apps.json_validate import SCHEMA
from config import config


class WechatSessionsHandler(BaseHandler):

    def post(self):
        is_valid, data = self.get_params_from_request(
            request, SCHEMA['wechat_sessions_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'])

        js_code = data['code']
        api_resp = requests.get(
            'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(
                config['wechat']['appId'], config['wechat']['appSecret'], js_code))
        resp_status = api_resp.status_code
        if resp_status != 200:
            self.logger.error('request wechat server failed')
            return '', 500

        open_id = api_resp.json().get('openid')
        session_key = api_resp.json().get('session_key')
        if not open_id or not session_key:
            err_msg = api_resp.json().get('errmsg')
            return self.error_msg(err_msg)

        # TODO: save open_id&session_key to db, add api in accounts
        # {'token': token, 'openid': 'openid', 'sessionKey': session_key}
        session = create_jwt({'openid': open_id}, session_key)
        return {'session': session}, 201
