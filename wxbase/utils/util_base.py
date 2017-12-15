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
