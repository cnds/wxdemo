from flask import request, jsonify
from jybase.utils import create_md5_key
from config import config
from .base import BaseHandler
from .json_validate import SCHEMA


class StoreInfoHandler(BaseHandler):

    def get(self, user_id, scene):
        flag, tag = self.authenticate(request, user_id, 
                                      create_md5_key(config['secret']))
        if not flag:
            return self.error_msg(tag)