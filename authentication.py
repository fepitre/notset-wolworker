import secrets
import jwt


class AuthClient:

    def __init__(self, key, uids):
        self._key = key
        self._uids = uids

    def create_token(self, uid=None):
        if not uid:
            uid = secrets.token_hex(16)
        token = jwt.encode({'uid': uid}, self._key).decode('utf8')
        creds = {
            "uid": str(uid),
            "token": token
        }
        return creds

    def decode_token(self, token):
        if token:
            try:
                data = jwt.decode(token, self._key)
                return data.get('uid')
            except:
                pass

    def valid_token(self, token):
        decoded_uid = self.decode_token(token)
        if not (decoded_uid or decoded_uid in self._uids):
            return False
        else:
            return True
