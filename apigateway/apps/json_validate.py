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
        "mobile": {"type": "string", "pattern": "^(1[3|5|7|8]\\d{9})$"}
    },
    "required": ["mobile", "password"],
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

wechat_sessions_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "code": {"type": "string"}
    },
    "required": ["code"],
    "additionalProperties": False
}


SCHEMA = {
    'stores_get': stores_get,
    'stores_post': stores_post,
    'store_sessions_post': store_sessions_post,
    'wechat_sessions_post': wechat_sessions_post,
}
