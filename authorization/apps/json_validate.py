stores_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "mobile": {"type": "string"},
    },
    "additionalProperties": False
}

stores_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "password": {"type": "string", "minLength": 8},
        "mobile": {"type": "string", "pattern": "^(1[3|5|7|8]\\d{9})$"},
        "code": {"type": "string"}
    },
    "required": ["mobile", "password", "code"],
    "additionalProperties": False
}

store_sessions_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "password": {"type": "string", "minLength": 8},
        "mobile": {"type": "string", "pattern": "^(1[3|5|7|8]\\d{9})$"}
    },
    "required": ["mobile", "password"],
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

sms_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "mobile": {"type": "string", "pattern": "^(1[3|5|7|8]\d{9})$"},
        "verifyType": {
            "type": "string",
            "enum": ["store_reset_password", "store_sign_up"]}
    },
    "required": ["verifyType", "mobile"],
    "additionalProperties": False
}

store_reset_password = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "newPassword": {"type": "string", "minLength": 8},
        "mobile": {"type": "string", "pattern": "^(1[3|5|7|8]\\d{9})$"},
        "code": {"type": "string"}
    },
    "required": ["mobile", "newPassword", "code"],
    "additionalProperties": False
}

user_sessions_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "openId": {"type": "string"},
    },
    "required": ["openId"],
    "additionalProperties": False
}

SCHEMA = {
    'stores_get': stores_get,
    'stores_post': stores_post,
    'store_sessions_post': store_sessions_post,
    'user_register_status_post': user_register_status_post,
    'sms_post': sms_post,
    'store_reset_password': store_reset_password,
    'user_sessions_post': user_sessions_post,
}
