transactions_post = {
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

transactions_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "userId": {"type": "string"},
        "skip": {"type": "integer", "minimum": 0, "excludeMinimum": False},
        "limit": {"type": "integer", "minimum": 0, "excludeMinimum": True}
    },
    "additionalProperties": False
}

transaction_get = {
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


SCHEMA = {
    'transactions_post': transactions_post,
    'transactions_get': transactions_get,
    'transaction_get': transaction_get,
    'promotions_put': promotions_put,
    'promotions_get': promotions_get,
}
