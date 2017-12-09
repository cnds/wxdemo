from flask.views import MethodView

from wxbase import MongoBase, RedisBase
from wxbase.utils import UtilBase
from config import config


class Base(MethodView, UtilBase):

    def __init__(self):
        super(Base, self).__init__()
        self.db = MongoBase(config)
        self.redis = RedisBase(config)
