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

store_reset_password_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "newPassword": {"type": "string", "minLength": 8},
        "code": {"type": "string"},
        "mobile": {"type": "string", "pattern": "^(1[3|5|7|8]\\d{9})$"}
    },
    "required": ["mobile", "newPassword", "code"],
    "additionalProperties": False
}

store_profiles_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {
            "oneOf": [
                {"type": "string"},
                {"type": "array"}
            ]
        }
    },
    "additionalProperties": False
}

store_profile_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "address": {"type": "string"},
        "name": {"type": "string"},
        "storeId": {"type": "string"},
    },
    "required": ["storeId"],
    "minProperties": 2,
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

SCHEMA = {
    'stores_get': stores_get,
    'stores_post': stores_post,
    'store_sessions_post': store_sessions_post,
    'store_reset_password_post': store_reset_password_post,
    'store_profiles_get': store_profiles_get,
    'store_profile_put': store_profile_put,
    'users_get': users_get,
    'users_post': users_post,
    'user_register_status_post': user_register_status_post,
    'user_sessions_post': users_sessions_post,
}
