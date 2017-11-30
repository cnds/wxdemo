from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from authorization.config import config
from authorization.apps.store_sessions_handle import StoreSessionsHandler


def create_app(config):
    app = Flask(__name__)
    app.config['TESTING'] = config['testing']
    app.config['DEBUG'] = config['debug']
    app.add_url_rule('/authorization/store-sessions',
                     view_func=StoreSessionsHandler.as_view('session'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    app = create_app(config)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), app).serve_forever()
