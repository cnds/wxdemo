from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from config import config
from apps.store_sessions_handle import StoreSessionsHandler
from apps.sms_handle import SmsHandler


def create_app(config):
    app = Flask(__name__)
    app.config['TESTING'] = config['testing']
    app.config['DEBUG'] = config['debug']
    app.add_url_rule('/authorization/store-sessions',
                     view_func=StoreSessionsHandler.as_view('session'))
    app.add_url_rule('/authorization/sms',
                     view_func=SmsHandler.as_view('sms'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    app = create_app(config)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), app).serve_forever()
