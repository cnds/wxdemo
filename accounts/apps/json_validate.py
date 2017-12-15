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

store_profile_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"}
    },
    "required": ["storeId"],
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


SCHEMA = {
    'stores_get': stores_get,
    'stores_post': stores_post,
    'store_sessions_post': store_sessions_post,
    'store_reset_password_post': store_reset_password_post,
    'store_profile_get': store_profile_get,
    'store_profile_put': store_profile_put,
}
