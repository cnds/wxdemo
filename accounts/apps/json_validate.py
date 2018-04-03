stores_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeName": {"type": "string"},
        "mobile": {"type": "string"},
        "id": {
            "oneOf": [
                {"type": "string"},
                {"type": "array"}
            ]
        }
    },
    "additionalProperties": False
}

stores_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "password": {"type": "string"},
        "mobile": {"type": "string", "pattern": "^(1[3|5|7|8]\\d{9})$"},
        "smsCode": {"type": "string"},
        "address": {"type": "string"},
        "storeName": {"type": "string"}
    },
    "required": ["mobile", "password", "smsCode", "address", "storeName"],
    "additionalProperties": False
}

store_sessions_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "password": {"type": "string"},
        "mobile": {"type": "string", "pattern": "^(1[3|5|7|8]\\d{9})$"}
    },
    "required": ["mobile", "password"],
    "additionalProperties": False
}

store_reset_password_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "newPassword": {"type": "string"},
        "smsCode": {"type": "string"},
        "mobile": {"type": "string", "pattern": "^(1[3|5|7|8]\\d{9})$"}
    },
    "required": ["mobile", "newPassword", "smsCode"],
    "additionalProperties": False
}

# store_profiles_get = {
#     "$schema": "http://json-schema.org/schema#",
#     "type": "object",
#     "properties": {
#         "storeId": {
#             "oneOf": [
#                 {"type": "string"},
#                 {"type": "array"}
#             ]
#         }
#     },
#     "additionalProperties": False
# }
#
# store_profile_put = {
#     "$schema": "http://json-schema.org/schema#",
#     "type": "object",
#     "properties": {
#         "address": {"type": "string"},
#         "storeName": {"type": "string"},
#         "storeId": {"type": "string"},
#     },
#     "required": ["storeId"],
#     "minProperties": 2,
#     "additionalProperties": False
# }

store_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "address": {"type": "string"},
        "storeName": {"type": "string"},
    },
    "minProperties": 1,
    "additionalProperties": False
}

users_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "openId": {"type": "string"},
        "id": {
            "oneOf": [
                {"type": "string"},
                {"type": "array"}
            ]
        }
    },
    "additionalProperties": False
}

users_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "code": {"type": "string"},
        "iv": {"type": "string"},
        "encryptedData": {"type": "string"}
    },
    "required": ["code", "iv", "encryptedData"],
    "additionalProperties": False
}

user_register_status_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "code": {"type": "string"}
    },
    "required": ["code"],
    "additionalProperties": False
}

users_sessions_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "openId": {"type": "string"}
    },
    "required": ["openId"],
    "additionalProperties": False
}

qr_code_bind_store_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "QRCode": {"type": "string"},
        "storeId": {"type": "string"}
    },
    "required": ["QRCode", "storeId"],
    "additionalProperties": False
}

store_bind_payment_info_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "wechatInfo": {"type": "string"},
        "alipayInfo": {"type": "string"},
        "storeId": {"type": "string"}
    },
    "required": ["storeId"],
    "minProperties": 2,
    "additionalProperties": False
}

qr_codes_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "code": {"type": "string"}
    },
    "additionalProperties": False
}

point_password_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "pointPassword": {"type": "string", "pattern": "^(\d{6})$"},
    },
    "minProperties": 1,
    "additionalProperties": False
}

point_password_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "pointPassword": {"type": "string", "pattern": "^(\d{6})$"},
    },
    "minProperties": 1,
    "additionalProperties": False
}


SCHEMA = {
    'stores_get': stores_get,
    'stores_post': stores_post,
    'store_sessions_post': store_sessions_post,
    'store_reset_password_post': store_reset_password_post,
    'users_get': users_get,
    'users_post': users_post,
    'user_register_status_post': user_register_status_post,
    'user_sessions_post': users_sessions_post,
    'qr_code_bind_store_post': qr_code_bind_store_post,
    'store_put': store_put,
    'qr_codes_get': qr_codes_get,
    'store_bind_payment_info_post': store_bind_payment_info_post,
    'point_password_post': point_password_post,
    'point_password_put': point_password_put,
}
