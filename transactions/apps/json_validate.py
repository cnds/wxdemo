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
        "reduction": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "excludeMinimum": True
        },
        "discount": {
            "type": "object",
            "properties": {
                "base": {
                    "type": "integer", "minimum": 0, "excludeMinimum": True},
                "minus": {
                    "type": "integer", "minimum": 0, "excludeMinimum": False}
            },
            "required": ["base", "minus"],
            "additionalProperties": False
        },
        "coupons": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "pay": {
                        "type": "integer", "minimum": 0, "excludeMinimum": False},
                    "base": {
                        "type": "integer", "minimum": 0, "excludeMinimum": True},
                    "minus": {
                        "type": "integer", "minimum": 0, "excludeMinimum": False}
                },
                "required": ["pay", "base", "minus"],
                "additionalProperties": False
            },
        },
    },
    "required": ["storeId"],
    "minProperties": 2,
    "additionalProperties": False
}

promotions_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
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
        "storeId": {"type": "string"}
    },
    "required": ["storeId"],
    "additionalProperties": False
}

coupons_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "pay": {"type": "integer", "minimum": 0, "excludeMinimum": False},
        "base": {"type": "integer", "minimum": 0, "excludeMinimum": False},
        "minus": {"type": "integer", "minimum": 0, "excludeMinimum": False},
    },
    "required": ["storeId", "pay", "base", "minus"],
    "additionalProperties": False
}

reductions_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
    },
    "additionalProperties": False
}

reductions_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "percent": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "excludeMinimum": True
        },
    },
    "required": ["storeId", "percent"],
    "additionalProperties": False
}

discounts_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
    },
    "additionalProperties": False
}

discounts_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "base": {"type": "integer", "minimum": 0},
        "minus": {"type": "integer", "minimum": 0}
    },
    "required": ["storeId", "base", "minus"],
    "additionalProperties": False
}

discount_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "base": {"type": "integer", "minimum": 0},
        "minus": {"type": "integer", "minimum": 0}
    },
    "required": ["storeId", "base", "minus"],
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
    'coupons_post': coupons_post,
    'reductions_put': reductions_put,
    'reductions_get': reductions_get,
    'discounts_get': discounts_get,
    'discount_put': discount_put,
}
