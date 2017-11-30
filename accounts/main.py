from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from accounts.apps.stores import Stores, Store
from accounts.apps.store_sessions import StoreSessions
from accounts.config import config

def create_app(config):
    app = Flask(__name__)
    app.config['DEBUG'] = config['debug']
    app.config['TESTING'] = config['testing']
    app.add_url_rule('/stores', view_func=Stores.as_view('stores'))
    app.add_url_rule('/stores/<store_id>', view_func=Store.as_view('store'))
    app.add_url_rule('/stores/sessions', view_func=StoreSessions.as_view('sessions'))
    return app


if __name__ == '__main__':
    app = create_app(config)
    api_port = config['api_port']
    print('Start listen on %s' % api_port)
    WSGIServer(('', api_port), app).serve_forever()