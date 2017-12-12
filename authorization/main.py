from gevent import monkey
from flask import Flask
from gevent.pywsgi import WSGIServer
from config import config
from apps.store_sessions_handle import StoreSessionsHandler
from apps.sms_handle import SmsHandler
from apps.stores_handle import StoresHandler, StoreResetPasswordHandler
monkey.patch_all()


def create_app(setting):
    app = Flask(__name__)
    app.config['TESTING'] = setting['testing']
    app.config['DEBUG'] = setting['debug']
    app.add_url_rule('/authorization/store-sessions',
                     view_func=StoreSessionsHandler.as_view('session'))
    app.add_url_rule('/authorization/sms',
                     view_func=SmsHandler.as_view('sms'))
    app.add_url_rule('/authorization/stores',
                     view_func=StoresHandler.as_view('stores'))
    app.add_url_rule('/authorization/stores/reset-password',
                     view_func=StoreResetPasswordHandler.as_view(
                         'store-reset-password'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    app = create_app(config)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), app).serve_forever()
