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
        "page": {"type": "integer", "minimum": 0, "excludeMinimum": True},
        "limit": {"type": "integer", "minimum": 0, "excludeMinimum": True},
    },
    "additionalProperties": False
}

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

user_orders_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "page": {"type": "integer", "minimum": 0, "excludeMinimum": True},
        "limit": {"type": "integer", "minimum": 0, "excludeMinimum": True},
    },
    "additionalProperties": False
}

store_bind_qr_code_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "QRCode": {"type": "string"}
    },
    "minProperties": 1,
    "additionalProperties": False
}

user_actual_amount_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "amount": {"type": "string"}
    },
    "required": ["storeId", "amount"],
    "additionalProperties": False
}

promotions_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "discount": {
            "type": "object",
            "properties": {
                "base": {"type": "integer", "minimum": 0, "excludeMinimum": True},
                "minus": {"type": "integer", "minimum": 0, "excludeMinimum": False}
            },
            "required": ["base", "minus"],
            "additionalProperties": False
        },
        "coupon": {
            "type": "object",
            "properties": {
                "pay": {"type": "integer", "minimum": 0, "excludeMinimum": True},
                "base": {"type": "integer", "minimum": 0, "excludeMinimum": True},
                "minus": {"type": "integer", "minimum": 0, "excludeMinimum": False}
            },
            "required": ["base", "minus"],
            "additionalProperties": False
        },
    },
    "minProperties": 1,
    "additionalProperties": False
}

coupons_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "pay": {"type": "integer", "minimum": 0, "excludeMinimum": True},
        "base": {"type": "integer", "minimum": 0, "excludeMinimum": True},
        "minus": {"type": "integer", "minimum": 0, "excludeMinimum": False}
    },
    "required": ["pay", "minus", "base"],
    "additionalProperties": False
}

coupon_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "pay": {"type": "integer", "minimum": 0, "excludeMinimum": True},
        "base": {"type": "integer", "minimum": 0, "excludeMinimum": True},
        "minus": {"type": "integer", "minimum": 0, "excludeMinimum": False}
    },
    "required": ["pay", "minus", "base"],
    "additionalProperties": False
}

SCHEMA = {
    'stores_get': stores_get,
    'stores_post': stores_post,
    'store_sessions_post': store_sessions_post,
    'store_put': store_put,
    'store_orders_get': store_orders_get,
    'user_orders_get': user_orders_get,
    'store_bind_qr_code_post': store_bind_qr_code_post,
    'user_actual_amount_post': user_actual_amount_post,
    'promotions_put': promotions_put,
    'coupons_post': coupons_post,
    'coupon_put': coupon_put,
}
