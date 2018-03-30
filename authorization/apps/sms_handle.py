import uuid
import json
from flask import request, jsonify
from .base import BaseHandler
from .json_validate import SCHEMA
from jybase.utils import generate_verification_code
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from config import config


class SmsHandler(BaseHandler):

    REGION = "cn-hangzhou"
    PRODUCT_NAME = "Dysmsapi"
    DOMAIN = "dysmsapi.aliyuncs.com"

    acs_client = AcsClient(config['sms']['access_key_id'],
                           config['sms']['access_key_secret'], REGION)
    region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

    # from aliyun demo
    def send_sms(self, business_id, phone_numbers, sign_name, template_code,
                 template_param=None):
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(template_code)

        # 短信模板变量参数
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)

        # 设置业务请求流水号，必填。
        smsRequest.set_OutId(business_id)

        # 短信签名
        smsRequest.set_SignName(sign_name)

        # 数据提交方式
        # smsRequest.set_method(MT.POST)

        # 数据提交格式
        # smsRequest.set_accept_format(FT.JSON)

        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)

        # 调用短信发送接口，返回json
        smsResponse = self.acs_client.do_action_with_exception(smsRequest)

        return json.loads(smsResponse)

    def post(self):
        is_valid, data = self.get_params_from_request(request,
                                                      SCHEMA['sms_post'])
        if not is_valid:
            return self.error_msg(self.ERR['invalid_body_content'], data)

        verify_type = data['verifyType']
        mobile = data['mobile']
        code = generate_verification_code(include_letter=False,
                                          include_upper=False)
        business_id = uuid.uuid1()
        params = json.dumps({'code': code})
        result = self.send_sms(business_id, mobile, config['sms']['sign'],
                               config['sms']['template'][verify_type], params)
        result_code = result['Code']
        if result_code == 'OK':
            redis_key = verify_type + ':' + mobile + ':'
            self.redis.set_value(redis_key, code)
            return jsonify({'id': result['RequestId']}), 201
