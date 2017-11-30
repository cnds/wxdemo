from flask import jsonify, logging
from flask.views import MethodView
from jsonschema import validate, ValidationError

from wxbase import MongoBase, RedisBase
from wxbase.utils import UtilBase
from accounts.config import config


class Base(MethodView, UtilBase):

    def __init__(self):
        super(Base, self).__init__()
        self.db = MongoBase(config)
        self.redis = RedisBase(config)
