promotions_put = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"},
        "promotions": {
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
                        "base": {"type": "integer", "minimum": 0, "excludeMinimum": True},
                        "minus": {"type": "integer", "minimum": 0, "excludeMinimum": False}
                    },
                    "required": ["base", "minus"],
                    "additionalProperties": False
                }
            },
            "minProperties": 1
        },
    },
    "required": ["storeId", "promotions"],
    "additionalProperties": False
}

promotions_get = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "storeId": {"type": "string"}
    },
    "additionalProperties": False
}


SCHEMA = {
    'promotions_put': promotions_put,
    'promotions_get': promotions_get,
}
