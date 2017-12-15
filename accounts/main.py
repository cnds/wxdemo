from gevent import monkey
from flask import Flask
from gevent.pywsgi import WSGIServer
from apps.stores import Stores, Store, StoreResetPassword
from apps.store_sessions import StoreSessions
from apps.store_profile import StoreProfile
from config import config
monkey.patch_all()


app = Flask(__name__)


def create_app(setting):
    app.config['DEBUG'] = setting['debug']
    app.config['TESTING'] = setting['testing']
    app.add_url_rule('/accounts/stores', view_func=Stores.as_view('stores'))
    app.add_url_rule('/accounts/stores/<store_id>', view_func=Store.as_view('store'))
    app.add_url_rule('/accounts/store-sessions',
                     view_func=StoreSessions.as_view('store-sessions'))
    app.add_url_rule('/accounts/stores/reset-password',
                     view_func=StoreResetPassword.as_view('reset-password'))
    app.add_url_rule('/accounts/stores/profile',
                     view_func=StoreProfile.as_view('store-profile'))
    return app


if __name__ == '__main__':
    app = create_app(config)
    api_port = config['api_port']
    print('Start listen on %s' % api_port)
    WSGIServer(('', api_port), app).serve_forever()
