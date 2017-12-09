from flask.views import MethodView
from wxbase import RedisBase
from wxbase.utils import UtilBase, RequestEndpoint
from config import config


class BaseHandler(MethodView, UtilBase):

    def __init__(self):
        super(BaseHandler, self).__init__()
        self.redis = RedisBase(config)
        self.endpoint = RequestEndpoint(config).endpoint
