from gevent import monkey
from flask import Flask
from gevent.pywsgi import WSGIServer
from config import config
from apps import Promotions
monkey.patch_all()


def create_app(setting):
    app = Flask(__name__)
    app.config['TESTING'] = setting['testing']
    app.config['DEBUG'] = setting['debug']
    app.add_url_rule('/promotions',
                     view_func=Promotions.as_view('session'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    app = create_app(config)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), app).serve_forever()
