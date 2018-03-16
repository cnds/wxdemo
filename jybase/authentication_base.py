from .utils import JWTBase


class AuthenticationBase(JWTBase):

    token_schema = {
        "$schema": "http://json-schema.org/schema#",
        "type": "object",
        "properties": {
            "accountId": {"type": "string"},
        },
        "minProperties": 1,
        "additionalProperties": False
    }

    def __init__(self):
        super().__init__()

    @staticmethod
    def check_route_id(params, token_id):
        id_name_list = ['store_id']
        route_id = 'store_id'
        for item in id_name_list:
            if params.get(item):
                route_id = params.get(item)
                break

        if route_id != token_id:
            return False

        return True

    @staticmethod
    def get_token_header(req):
        token_header = req.environ.get('HTTP_AUTHORIZATION')
        if token_header:
            token = token_header.split(' ')
            token = token[1] if len(token) == 2 else None
            if not token:
                return False, None

        else:
            return False, None

        return True, token

    @staticmethod
    def check_account_type(account_type, expected_type):
        if isinstance(expected_type, str):
            expected_type = (expected_type,)

        if not isinstance(expected_type, tuple):
            raise Exception

        if account_type not in expected_type:
            return False

        return True

    def authenticate(self, req, entity_id, secret, schema=token_schema,
                     verify_expiration=True):
        flag, token = self.get_token_header(req)
        if not flag:
            return False, self.ERR['authentication_info_required']

        flag, token_content = self.check_jwt(
            token, secret, schema=schema, verify_expiration=verify_expiration)
        if not flag:
            return False, self.ERR['authentication_info_illegal']

        token_id = token_content['accountId']
        if token_id != entity_id:
            return False, self.ERR['permission_denied']

        return True, None
