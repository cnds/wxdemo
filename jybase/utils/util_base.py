from flask import jsonify, logging
from jsonschema import validate, ValidationError


class UtilBase(object):

    _error_msg = {
        'invalid_body_content': 'INVALID_BODY_CONTENT',
        'invalid_query_params': 'INVALID_QUERY_PARAMS',
        'conflict_user_exist': 'CONFLICT_USER_EXIST',
        'user_not_found': 'USER_NOT_FOUND',
        'not_found': 'NOT_FOUND',
        'password_verification_failed': 'PASSWORD_VERIFICATION_FAILED',
        'sms_code_verification_failed': 'SMS_CODE_VERIFICATION_FAILED',
        'attempt_too_many_times': 'ATTEMPT_TOO_MANY_TIMES',
        'authentication_info_required': 'AUTHENTICATION_INFO_REQUIRED',
        'authentication_info_illegal': 'AUTHENTICATION_INFO_ILLEGAL',
        'permission_denied': 'PERMISSION_DENIED',
        'operation_failed': 'OPERATION_FAILED',
        'invalid_wx_code': 'INVALID_WX_CODE',
        'qr_code_not_exist': 'QR_CODE_NOT_EXIST',
        'store_not_exist': 'STORE_NOT_EXIST',
        'qr_code_already_been_bound': 'QR_CODE_ALREADY_BEEN_BOUND',
        'conflict_coupon': 'CONFLICT_COUPON',
        'coupon_not_exist': 'COUPON_NOT_EXIST',
        'coupon_has_been_removed': 'COUPON_HAS_BEEN_REMOVED',
        'promotion_not_exist': 'PROMOTION_NOT_EXIST',
        'db_bulk_update_error': 'DB_BULK_UPDATE_ERROR',
        'conflict_discount': 'CONFLICT_DISCOUNT',
        'discount_not_exist': 'DISCOUNT_NOT_EXIST',
        'discount_has_been_removed': 'DISCOUNT_HAS_BEEN_REMOVED',
        'reduction_has_been_removed': 'REDUCTION_HAS_BEEN_REMOVED',
        'reduction_not_exist': 'REDUCTION_NOT_EXIST',
        'user_coupon_not_exist': 'USER_COUPON_NOT_EXIST',
        'store_have_not_bound_qr_code': 'STORE_HAVE_NOT_BOUND_QR_CODE',
        'password_been_set': 'PASSWORD_BEEN_SET',
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ERR = self._error_msg

    @staticmethod
    def error_msg(msg, detail=None, status=400):
        result = {'error': msg}
        if detail:
            result.update({'detail': detail})

        return jsonify(result), status

    def validate_dict_with_schema(self, data, schema):
        try:
            validate(data, schema)
        except ValidationError as ex:
            self.logger.error(ex)
            return False, str(ex)

        return True, None

    def get_params_from_request(self, data, schema):
        try:
            params = data.get_json()
        except Exception as ex:
            return False, 'parse json failed: %s' % ex
        else:
            if params is None:
                return False, 'json required'
            is_valid, tag = self.validate_dict_with_schema(params, schema)
            if not is_valid:
                return False, tag

            return True, params

    @staticmethod
    def str_to_int(data, raise_value_error=False):
        if not isinstance(data, dict):
            return False, '<%s> is not dict type' % type(data)

        for k, v in data.items():
            try:
                data[k] = int(v)
            except ValueError:
                if raise_value_error:
                    return False, \
                           '%s type <%s> can not convert to <int>' % (
                               data, type(data))
                else:
                    pass

        return True, None

    @staticmethod
    def get_data_with_keys(data, keys=None, additional_data=None):
        if additional_data and not isinstance(additional_data, dict):
            raise Exception

        if keys:
            if not isinstance(keys, tuple):
                raise Exception

            result = {key: data[key] for key in keys if key in data}
        else:
            result = data

        if additional_data:
            result.update(additional_data)

        return result
