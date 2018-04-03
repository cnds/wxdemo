from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from config import config
from apps import PromotionsHandler, StoreOrdersHandler, \
    StoreOrderHandler, UserOrdersHandler, UserOrderHandler, \
    StoreBindQRCodeHandler, UserPaymentDetailHandler, StoreHandler, \
    StoreCouponsHandler, StoreCouponHandler, \
    StoreDiscountsHandler, StoreDiscountHandler, \
    StoreReductionsHandler, StoreReductionHandler, \
    UserCouponsHandler, UserCouponRemoverHandler, StoreBindPaymentInfoHandler, \
    QRCodes, StoreInfoHandler, StorePointPassword


def create_app(setting):
    app = Flask(__name__)
    app.config['TESTING'] = setting['testing']
    app.config['DEBUG'] = setting['debug']

    # NOTE: stores
    app.add_url_rule('/gateway/stores/<store_id>/promotions',
                     view_func=PromotionsHandler.as_view('promotions'))
    app.add_url_rule('/gateway/stores/<store_id>/orders',
                     view_func=StoreOrdersHandler.as_view('store-orders'))
    app.add_url_rule('/gateway/stores/<store_id>/orders/<order_id>',
                     view_func=StoreOrderHandler.as_view('store-order'))
    app.add_url_rule('/gateway/stores/<store_id>',
                     view_func=StoreHandler.as_view('store'))
    app.add_url_rule('/gateway/stores/<store_id>/bind-qr-code',
                     view_func=StoreBindQRCodeHandler.as_view('store-bind-qr-code'))
    app.add_url_rule('/gateway/stores/<store_id>/bind-payment-info',
                     view_func=StoreBindPaymentInfoHandler.as_view('store-bind-payment-info'))
    app.add_url_rule('/gateway/stores/<store_id>/coupons',
                     view_func=StoreCouponsHandler.as_view('store-coupons'))
    app.add_url_rule('/gateway/stores/<store_id>/coupons/<coupon_id>',
                     view_func=StoreCouponHandler.as_view('store-coupon'))
    app.add_url_rule('/gateway/stores/<store_id>/discounts',
                     view_func=StoreDiscountsHandler.as_view('store-discounts'))
    app.add_url_rule('/gateway/stores/<store_id>/discounts/<discount_id>',
                     view_func=StoreDiscountHandler.as_view('store-discount'))
    app.add_url_rule('/gateway/stores/<store_id>/reductions',
                     view_func=StoreReductionsHandler.as_view('store-reductions'))
    app.add_url_rule('/gateway/stores/<store_id>/reductions/<reduction_id>',
                     view_func=StoreReductionHandler.as_view('store-reduction'))
    app.add_url_rule('/gateway/stores/<store_id>/qr-code',
                     view_func=QRCodes.as_view('qr-codes'))
    app.add_url_rule('/gateway/stores/<store_id>/point-password',
                     view_func=StorePointPassword.as_view('store-point-password'))

    # NOTE: users
    app.add_url_rule('/gateway/users/<user_id>/orders',
                     view_func=UserOrdersHandler.as_view('user-orders'))
    app.add_url_rule('/gateway/users/<user_id>/orders/<order_id>',
                     view_func=UserOrderHandler.as_view('user-order'))
    app.add_url_rule('/gateway/users/<user_id>/payment-detail',
                     view_func=UserPaymentDetailHandler.as_view('payment-detail'))
    app.add_url_rule('/gateway/users/<user_id>/coupons',
                     view_func=UserCouponsHandler.as_view('user-coupons'))
    app.add_url_rule('/gateway/users/<user_id>/coupons/remove',
                     view_func=UserCouponRemoverHandler.as_view('user-coupon-remover'))
    app.add_url_rule('/gateway/users/<user_id>/store-info/<code>',
                     view_func=StoreInfoHandler.as_view('store-info'))
    return app


if __name__ == '__main__':
    api_port = config['api_port']
    application = create_app(config)
    print('Start liston on %s' % api_port)
    WSGIServer(('', api_port), application).serve_forever()
