from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from config import config
from apps import Coupons, Coupon, Promotion, Reductions, Reduction, \
    Discounts, Discount, Orders, Order, Promotions, ActualAmount


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
    app.add_url_rule('/transactions/promotions/<promotion_id>',
                     view_func=Promotion.as_view('promotion'))
    app.add_url_rule('/transactions/discounts',
                     view_func=Discounts.as_view('discounts'))
    app.add_url_rule('/transactions/discounts/<discount_id>',
                     view_func=Discount.as_view('discount'))
    app.add_url_rule('/transactions/coupons',
                     view_func=Coupons.as_view('coupons'))
    app.add_url_rule('/transactions/coupons/<coupon_id>',
                     view_func=Coupon.as_view('coupon'))
    app.add_url_rule('/transactions/reductions',
                     view_func=Reductions.as_view('reductions'))
    app.add_url_rule('/transactions/reductions/<reduction_id>',
                     view_func=Reduction.as_view('reduction'))
    app.add_url_rule('/transactions/actual-amount',
                     view_func=ActualAmount.as_view('actual-amount'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    application = create_app(config)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), application).serve_forever()
