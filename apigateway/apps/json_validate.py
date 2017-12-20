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

store_orders_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "skip": {"type": "integer", "minimum": 0, "excludeMinimum": False},
        "limit": {"type": "integer", "minimum": 0, "excludeMinimum": True},
    },
    "additionalProperties": False
}

store_profile_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "address": {"type": "string"},
        "name": {"type": "string"},
    },
    "minProperties": 1,
    "additionalProperties": False
}

user_orders_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "skip": {"type": "integer", "minimum": 0, "excludeMinimum": False},
        "limit": {"type": "integer", "minimum": 0, "excludeMinimum": True},
    },
    "additionalProperties": False
}

SCHEMA = {
    'stores_get': stores_get,
    'stores_post': stores_post,
    'store_sessions_post': store_sessions_post,
    'store_profile_put': store_profile_put,
    'store_orders_get': store_orders_get,
    'user_orders_get': user_orders_get,
}
