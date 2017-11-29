from redis import Redis
from flask import logging


class RedisBase(object):

    ONE_DAY_IN_SECONDS = 60*60*24

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.redis = self.init_redis(config)

    def init_redis(self, config):
        self._redis = Redis(config['redis']['host'], config['redis']['port'])
        return self._redis

    def set_ip_block(self, remote_ip):
        key = 'ip_block:%s' % remote_ip
        try:
            result = self.redis.incr(key)
            self.redis.expire(key, self.ONE_DAY_IN_SECONDS)
        except Exception as ex:
            self.logger.error(ex)
            return False
        else:
            return True if result == 1 else False
