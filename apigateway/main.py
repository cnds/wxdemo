from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from config import config
from apps import PromotionsHandler, StoreOrdersHandler, \
    StoreOrderHandler, StoreProfileHandler, \
    UserOrdersHandler, UserOrderHandler, StoreBindQRCodeHandler, \
    UserActualAmountHandler


def create_app(setting):
    app = Flask(__name__)
    app.config['TESTING'] = setting['testing']
    app.config['DEBUG'] = setting['debug']

    #NOTE: stores
    app.add_url_rule('/gateway/stores/<store_id>/promotions',
                     view_func=PromotionsHandler.as_view('promotions'))
    app.add_url_rule('/gateway/stores/<store_id>/orders',
                     view_func=StoreOrdersHandler.as_view('store-orders'))
    app.add_url_rule('/gateway/stores/<store_id>/orders`/<order_id>',
                     view_func=StoreOrderHandler.as_view('store-order'))
    app.add_url_rule('/gateway/stores/<store_id>/profile',
                     view_func=StoreProfileHandler.as_view('store-profile'))
    app.add_url_rule('/gateway/stores/<store_id>/bind-qr-code',
                     view_func=StoreBindQRCodeHandler.as_view('store-bind-qr-code'))

    #NOTE: users
    app.add_url_rule('/gateway/users/<user_id>/orders',
                     view_func=UserOrdersHandler.as_view('user-orders'))
    app.add_url_rule('/gateway/users/<user_id>/orders/<order_id>',
                     view_func=UserOrderHandler.as_view('user-order'))
    app.add_url_rule('/gateway/users/<user_id>/actual-amount',
                     view_func=UserActualAmountHandler.as_view('actual-amount'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    application = create_app(config)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), application).serve_forever()
