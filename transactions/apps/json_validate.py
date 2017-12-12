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
        "userId": {"type": "string"}
    },
    "additionalProperties": False
}


SCHEMA = {
    'transactions_post': transactions_post,
    'transactions_get': transactions_get,
}
