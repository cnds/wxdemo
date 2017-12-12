from flask.views import MethodView
from wxbase import RedisBase, MongoBase
from wxbase.utils import UtilBase, RequestEndpoint
from config import config


class Base(MethodView, UtilBase):

    def __init__(self):
        super(Base, self).__init__()
        self.redis = RedisBase(config)
        self.db = MongoBase(config)
        self.endpoint = RequestEndpoint(config).endpoint
