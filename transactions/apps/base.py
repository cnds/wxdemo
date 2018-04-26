import requests
from flask.views import MethodView
from jybase import RedisBase, MongoBase
from jybase.utils import UtilBase, RequestEndpoint
from config import config


class Base(MethodView, UtilBase):

    def __init__(self):
        super(Base, self).__init__()
        self.redis = RedisBase(config)
        self.db = MongoBase(config)
        self.endpoint = RequestEndpoint(config).endpoint

    def get_access_token(self, app_id, secret):
        resp = requests.get(
            'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'.format(app_id, secret))
        token = resp.json().get('access_token')
        if not token:
            error_msg = resp.json().get('errmsg')
            self.logger.error('get access token failed: %s' % error_msg)
            return False

        return token

    def send_template_message(self, access_token, open_id, template_id, page, form_id, data):
        url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token={0}'.format(access_token)
        resp = requests.post(url, json={'touser': open_id, 'template_id': template_id,
                                 'page': page, 'form_id': form_id, 'data': data})
        code = resp.json().get('errcode')
        if code != 0:
            self.logger.error('send template message failed: %s' % resp.json().get('errmsg'))
            return False

        return True
