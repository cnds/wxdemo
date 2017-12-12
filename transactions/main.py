from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from config import config
from apps import Transactions, Transaction


def create_app(config):
    app = Flask(__name__)
    app.config['TESTING'] = config['testing']
    app.config['DEBUG'] = config['debug']
    app.add_url_rule('/transactions',
                     view_func=Transactions.as_view('transactions'))
    app.add_url_rule('/transactions/<transaction_id>',
                     view_func=Transaction.as_view('transaction'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    app = create_app(config)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), app).serve_forever()
