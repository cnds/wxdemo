from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from config import config
from apps import StoreSessionsHandler, SmsHandler, \
    StoresHandler, StoreResetPasswordHandler, \
    UserRegisterStatusHandler, UserSessionsHandler, UsersHandler


def create_app(setting):
    app = Flask(__name__)
    app.config['TESTING'] = setting['testing']
    app.config['DEBUG'] = setting['debug']
    app.add_url_rule('/authorization/store-sessions',
                     view_func=StoreSessionsHandler.as_view('store-session'))
    app.add_url_rule('/authorization/sms',
                     view_func=SmsHandler.as_view('sms'))
    app.add_url_rule('/authorization/stores',
                     view_func=StoresHandler.as_view('stores'))
    app.add_url_rule('/authorization/stores/reset-password',
                     view_func=StoreResetPasswordHandler.as_view(
                         'store-reset-password'))
    app.add_url_rule('/authorization/users/register-status',
                     view_func=UserRegisterStatusHandler.as_view(
                         'user-register-status'))
    app.add_url_rule('/authorization/user-sessions',
                     view_func=UserSessionsHandler.as_view('user-session'))
    app.add_url_rule('/authorization/users',
                     view_func=UsersHandler.as_view('users'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    application = create_app(config)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), application).serve_forever()
