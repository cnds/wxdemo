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

user_orders_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "amount": {"type": "integer", "minimum": 0, "excludeMinimum": True},
    },
    "required": ["storeId", "amount"],
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

store_bind_payment_info_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "wechatInfo": {"type": "string"},
        "alipayInfo": {"type": "string"}
    },
    "minProperties": 1,
    "additionalProperties": False
}

user_payment_detail_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "amount": {"type": "number"}
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

store_coupons_post = {
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

store_coupon_put = {
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

store_discounts_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "base": {"type": "integer", "minimum": 0, "excludeMinimum": True},
        "minus": {"type": "integer", "minimum": 0, "excludeMinimum": False}
    },
    "required": ["minus", "base"],
    "additionalProperties": False
}

store_discount_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "base": {"type": "integer", "minimum": 0, "excludeMinimum": True},
        "minus": {"type": "integer", "minimum": 0, "excludeMinimum": False}
    },
    "required": ["minus", "base"],
    "additionalProperties": False
}

user_coupons_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "amount": {"type": "integer", "minimum": 0, "excludeMinimum": True},
    },
    "required": ["storeId", "amount"],
    "additionalProperties": False
}

user_coupon_remover_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "couponId": {"type": "string"}
    },
    "required": ["storeId", "couponId"],
    "additionalProperties": False
}

store_reductions_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "percent": {"type": "integer", "minimum": 0, "maximum": 100, "excludeMinimum": True},
    },
    "required": ["percent"],
    "additionalProperties": False
}

store_point_password_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "pointPassword": {"type": "string", "pattern": "^(\d{6})$"},
    },
    "minProperties": 1,
    "additionalProperties": False
}

store_point_password_put = {
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
    'store_put': store_put,
    'store_orders_get': store_orders_get,
    'user_orders_get': user_orders_get,
    'user_orders_post': user_orders_post,
    'store_bind_qr_code_post': store_bind_qr_code_post,
    'user_payment_detail_post': user_payment_detail_post,
    'promotions_put': promotions_put,
    'store_reductions_put': store_reductions_put,
    'store_coupons_post': store_coupons_post,
    'store_coupon_put': store_coupon_put,
    'store_discounts_post': store_discounts_post,
    'store_discount_put': store_discount_put,
    'user_coupons_put': user_coupons_put,
    'user_coupon_remover_post': user_coupon_remover_post,
    'store_bind_payment_info_post': store_bind_payment_info_post,
    'store_point_password_post': store_point_password_post,
    'store_point_password_put': store_point_password_put,
}
