from flask import logging


class RequestEndpoint(object):
    BASE_URL = 'http://%s:%s'
    ENDPOINT = dict()

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.init(config)

    def init(self, config):
        if not self.ENDPOINT and config.get('service'):
            for service, entry in config['service'].items():
                self.ENDPOINT[service] = self.BASE_URL % (entry['host'],
                                                            entry['port'])

    @property
    def endpoint(self):
        return self.ENDPOINT
