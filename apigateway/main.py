from gevent import monkey
from flask import Flask
from gevent.pywsgi import WSGIServer
from config import config
from apps.promotions_handle import PromotionsHandler
from apps.store_transactions_handle import (StoreTransactionsHandler,
                                            StoreTransactionHandler)
monkey.patch_all()


def create_app(setting):
    app = Flask(__name__)
    app.config['TESTING'] = setting['testing']
    app.config['DEBUG'] = setting['debug']
    app.add_url_rule('/gateway/stores/<store_id>/promotions',
                     view_func=PromotionsHandler.as_view('promotions'))
    app.add_url_rule('/gateway/stores/<store_id>/transactions',
                     view_func=StoreTransactionsHandler.as_view('transactions'))
    app.add_url_rule('/gateway/stores/<store_id>/transactions/<transaction_id>',
                     view_func=StoreTransactionHandler.as_view('transaction'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    app = create_app(config)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), app).serve_forever()
