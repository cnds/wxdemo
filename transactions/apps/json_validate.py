orders_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "userId": {"type": "string"},
        "amount": {"type": "integer", "minimum": 0, "excludeMinimum": True}
    },
    "required": ["storeId", "userId", "amount"],
    "additionalProperties": False
}

orders_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "userId": {"type": "string"},
        "page": {"type": "integer", "minimum": 0, "excludeMinimum": True},
        "limit": {"type": "integer", "minimum": 0, "excludeMinimum": True}
    },
    "additionalProperties": False
}

order_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "userId": {"type": "string"},
    },
    "additionalProperties": False
}

promotions_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
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
                "pay": {"type": "integer", "minimum": 0, "excludeMinimum": False},
                "base": {"type": "integer", "minimum": 0, "excludeMinimum": True},
                "minus": {"type": "integer", "minimum": 0, "excludeMinimum": False}
            },
            "required": ["base", "minus"],
            "additionalProperties": False
        },
    },
    "required": ["storeId"],
    "additionalProperties": False
}

promotions_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"}
    },
    "required": ["storeId"],
    "additionalProperties": False
}

actual_amount_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "userId": {"type": "string"},
        "amount": {"type": "integer"}
    },
    "required": ["storeId", "userId", "amount"],
    "additionalProperties": False
}

coupons_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "userId": {"type": "string"}
    },
    "required": ["userId"],
    "additionalProperties": False
}


SCHEMA = {
    'orders_post': orders_post,
    'orders_get': orders_get,
    'order_get': order_get,
    'promotions_put': promotions_put,
    'promotions_get': promotions_get,
    'actual_amount_post': actual_amount_post,
    'coupons_get': coupons_get,
}
