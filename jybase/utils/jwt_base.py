import jwt
import json
import logging

from datetime import timedelta, datetime

from .util_base import UtilBase


class JWTBase(UtilBase):

    def __init__(self):
        super().__init__()

    @staticmethod
    def create_jwt(data, secret, algorithm='HS256', expire_day=7):
        """ set default algorithm and expire time"""
        expire_time = timedelta(days=expire_day)
        json_content = {
            'exp': datetime.utcnow() + expire_time,
            'body': data
        }
        token = jwt.encode(json_content, secret, algorithm)
        return token

    @staticmethod
    def decode_jwt(token, secret, algorithm='HS256', verify_expiration=True):
        try:
            data_decrypted = jwt.decode(token, secret, algorithm=algorithm,
                                        verify_expiration=verify_expiration)

        except Exception as ex:
            if ex == jwt.ExpiredSignature:
                logging.error('jwt expired signature error: %s' % ex)
            elif ex == jwt.DecodeError:
                logging.error('jwt decode error: %s' % ex)
            else:
                logging.error('unknown error: %s' % ex)

            return False, None

        else:
            return True, data_decrypted

    def check_token_content(self, data_from_client, data_from_decrypt, schema):
        '''
            Could be implemented in subclass
        '''
        try:
            data_from_client = json.loads(data_from_client)
        except Exception as ex:
            logging.error('parse failed: %s' % ex)
            return False

        flag, tag = self.validate_dict_with_schema(data_from_client['body'],
                                                   schema=schema)
        if not flag:
            return False

        flag, tag = self.validate_dict_with_schema(data_from_decrypt['body'],
                                                   schema=schema)
        if not flag:
            return False

        for key, value in data_from_client['body'].items():
            if data_from_decrypt['body'][key] == value:
                continue
            else:
                return False

        return True

    def check_jwt(self, token, secret, schema, verify_expiration=True):
        token_list = token.split('.')
        if len(token_list) != 3:
            return False, None

        data_receive = jwt.utils.base64url_decode(token_list[1])
        flag, data_decrypt = self.decode_jwt(
            token, secret, verify_expiration=verify_expiration)
        if not flag:
            return False, None

        flag = self.check_token_content(data_receive, data_decrypt, schema)
        if not flag:
            return False, None

        return True, data_decrypt['body']
