from flask import request, jsonify
from apps.base import BaseHandler
from apps.json_validate import SCHEMA
from jybase.utils import generate_verification_code


class SmsHandler(BaseHandler):

    sms_info = {
        'store_reset_password': '您正在申请重置商户密码, 验证码是%s, 有效期5分钟。',
        'store_sign_up': '您正在注册商户账号, 验证码是%s, 有效期5分钟。',
    }

    def send_sms(self, mobile, verify_type):
        code = generate_verification_code(include_letter=False,
                                          include_upper=False)
        text = self.sms_info.get(verify_type) % code
        print(text)
        redis_key = verify_type + ':' + mobile + ':'
        self.redis.set_value(redis_key, code)
        # TODO: send sms via sms service
        # send_sms_function(text)
        return True

    def post(self):
        is_valid, data = self.get_params_from_request(request,
                                                      SCHEMA['sms_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        verify_type = data['verifyType']
        mobile = data['mobile']
        result = self.send_sms(mobile, verify_type)
        if result:
            return jsonify({'id': verify_type}), 201
