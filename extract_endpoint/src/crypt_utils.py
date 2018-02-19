import secrets
import hmac
import base64


def get_salt(num_bytes=64) -> str:
    return base64.b64encode(secrets.token_bytes(num_bytes)).decode('utf-8')


def sign_string(salt: str, key: str, data: str) -> str:
    hash_key = (salt + key).encode('utf-8')
    hashed_data = hmac.new(bytes(hash_key), data.encode('utf-8'))
    return hashed_data.hexdigest()
