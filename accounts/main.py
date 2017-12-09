from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from apps.stores import Stores, Store, StoreResetPassword
from apps.store_sessions import StoreSessions
from config import config

def create_app(config):
    app = Flask(__name__)
    app.config['DEBUG'] = config['debug']
    app.config['TESTING'] = config['testing']
    app.add_url_rule('/accounts/stores', view_func=Stores.as_view('stores'))
    app.add_url_rule('/accounts/stores/<store_id>', view_func=Store.as_view('store'))
    app.add_url_rule('/accounts/store-sessions',
                     view_func=StoreSessions.as_view('store-sessions'))
    app.add_url_rule('/accounts/stores/reset-password',
                     view_func=StoreResetPassword.as_view('reset-password'))
    return app


if __name__ == '__main__':
    app = create_app(config)
    api_port = config['api_port']
    print('Start listen on %s' % api_port)
    WSGIServer(('', api_port), app).serve_forever()
