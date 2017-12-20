from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent.pywsgi import WSGIServer
from .apps import Stores, Store, StoreResetPassword, \
    StoreSessions, StoreProfile, StoreProfiles, \
    Users, UserRegisterStatus, UserSessions
from .config import config


app = Flask(__name__)


def create_app(setting):
    app.config['DEBUG'] = setting['debug']
    app.config['TESTING'] = setting['testing']
    app.add_url_rule('/accounts/stores', view_func=Stores.as_view('stores'))
    app.add_url_rule('/accounts/stores/<store_id>', view_func=Store.as_view('store'))
    app.add_url_rule('/accounts/store-sessions',
                     view_func=StoreSessions.as_view('store-sessions'))
    app.add_url_rule('/accounts/stores/reset-password',
                     view_func=StoreResetPassword.as_view('reset-password'))
    app.add_url_rule('/accounts/stores/<store_id>/profile',
                     view_func=StoreProfile.as_view('store-profile'))
    app.add_url_rule('/accounts/stores/profile',
                     view_func=StoreProfiles.as_view('store-profiles'))
    app.add_url_rule('/accounts/users',
                     view_func=Users.as_view('users'))
    app.add_url_rule('/accounts/users/register-status',
                     view_func=UserRegisterStatus.as_view('user-register-status'))
    app.add_url_rule('/accounts/user-sessions',
                     view_func=UserSessions.as_view('user-sessions'))
    return app


if __name__ == '__main__':
    app = create_app(config)
    api_port = config['api_port']
    print('Start listen on %s' % api_port)
    WSGIServer(('', api_port), app).serve_forever()
