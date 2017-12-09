from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from config import config
from apps.promotions_handle import PromotionsHandler


def create_app(config):
    app = Flask(__name__)
    app.config['TESTING'] = config['testing']
    app.config['DEBUG'] = config['debug']
    app.add_url_rule('/gateway/stores/<store_id>/promotions',
                     view_func=PromotionsHandler.as_view('promotions'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    app = create_app(config)
    print(app.url_map)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), app).serve_forever()
