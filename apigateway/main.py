from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from .config import config
from .apps import PromotionsHandler, StoreTransactionsHandler, \
    StoreTransactionHandler, StoreProfileHandler, \
    UserTransactionsHandler, UserTransactionHandler


def create_app(setting):
    app = Flask(__name__)
    app.config['TESTING'] = setting['testing']
    app.config['DEBUG'] = setting['debug']
    app.add_url_rule('/gateway/stores/<store_id>/promotions',
                     view_func=PromotionsHandler.as_view('promotions'))
    app.add_url_rule('/gateway/stores/<store_id>/transactions',
                     view_func=StoreTransactionsHandler.as_view('store-transactions'))
    app.add_url_rule('/gateway/stores/<store_id>/transactions/<transaction_id>',
                     view_func=StoreTransactionHandler.as_view('store-transaction'))
    app.add_url_rule('/gateway/stores/<store_id>/profile',
                     view_func=StoreProfileHandler.as_view('store-profile'))
    app.add_url_rule('/gateway/users/<user_id>/transactions',
                     view_func=UserTransactionsHandler.as_view('user-transactions'))
    app.add_url_rule('/gateway/users/<user_id>/transactions/<transaction_id>',
                     view_func=UserTransactionHandler.as_view('user-transaction'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    app = create_app(config)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), app).serve_forever()
