from flask.views import MethodView

from wxbase import MongoBase, RedisBase
from wxbase.utils import JWTBase
from config import config


class Base(MethodView, JWTBase):

    def __init__(self):
        super().__init__()
        self.db = MongoBase(config)
        self.redis = RedisBase(config)
