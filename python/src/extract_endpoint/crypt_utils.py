import os
import hmac
import base64


def get_salt(num_bytes=64) -> str:
    return base64.b64encode(os.urandom(num_bytes)).decode('utf-8')


def sign_data(salt: str, key: str, data: str) -> str:
    hash_key = (salt + key).encode('utf-8')
    hashed_data = hmac.new(bytes(hash_key), data.encode('utf-8'))
    return hashed_data.hexdigest()
