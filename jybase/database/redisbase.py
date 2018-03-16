from redis import Redis
from flask import logging


class RedisBase(object):

    ONE_DAY_IN_SECONDS = 60*60*24

    _redis_string = {
        'srp': 'store_reset_password:',
        'ssu': 'store_sign_up:'
    }

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.init_redis(config)
        self.REDIS_STRING = self._redis_string

    def init_redis(self, config):
        self._redis = Redis(config['redis']['host'], config['redis']['port'])
        return self._redis

    def set_ip_block(self, remote_ip):
        key = 'ip_block:%s' % remote_ip
        try:
            result = self._redis.incr(key)
            self._redis.expire(key, self.ONE_DAY_IN_SECONDS)
        except Exception as ex:
            self.logger.error(ex)
            return False
        else:
            return True if result == 1 else False

    def check_if_block(self, remote_ip, times=5):
        key = 'ip_block:%s' % remote_ip
        result = self.get_value(key)
        if result:
            return True if int(result) >= times else False
        else:
            return False

    def set_value(self, name, value, time=300):
        try:
            self._redis.setex(name, value, time)
        except Exception as ex:
            self.logger.error(ex)
            return False
        else:
            return True

    def get_value(self, name):
        try:
            result = self._redis.get(name)
        except Exception as ex:
            self.logger.error(ex)
            return False
        else:
            return result.decode() if result else None

