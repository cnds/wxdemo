from flask.views import MethodView
from wxbase import RedisBase, AuthenticationBase
from wxbase.utils import RequestEndpoint
from config import config


class BaseHandler(MethodView, AuthenticationBase):

    def __init__(self):
        super(BaseHandler, self).__init__()
        self.redis = RedisBase(config)
        self.endpoint = RequestEndpoint(config).endpoint
