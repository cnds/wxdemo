from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from config import config
from apps import Orders, Order, Promotions


def create_app(config):
    app = Flask(__name__)
    app.config['TESTING'] = config['testing']
    app.config['DEBUG'] = config['debug']
    app.add_url_rule('/transactions/orders',
                     view_func=Orders.as_view('orders'))
    app.add_url_rule('/transactions/orders/<order_id>',
                     view_func=Order.as_view('order'))
    app.add_url_rule('/transactions/promotions',
                     view_func=Promotions.as_view('promotions'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    application = create_app(config)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), application).serve_forever()
