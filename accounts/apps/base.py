import requests
from flask.views import MethodView

from jybase import MongoBase, RedisBase
from jybase.utils import JWTBase
from config import config


class Base(MethodView, JWTBase):

    def __init__(self):
        super().__init__()
        self.db = MongoBase(config)
        self.redis = RedisBase(config)

    def get_data_from_wx(self, app_id, secret, code):
        query_params = {
            'appid': app_id,
            'secret': secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        api_resp = requests.get(
            'https://api.weixin.qq.com/sns/jscode2session',
            params=query_params)
        resp_status = api_resp.status_code
        if resp_status != 200:
            self.logger('request wechat server failed')
            return False, None

        data_from_wx = api_resp.json()
        if not data_from_wx.get('openid') \
                and not data_from_wx.get('session_key'):
            return True, None

        return True, data_from_wx
