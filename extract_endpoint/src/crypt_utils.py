import hmac
import typing


def sign_string(salt: typing.Optional[str], key: str, data: str) -> str:
    salt = salt if salt is not None else ''
    hash_key = (salt + key).encode('utf-8')
    hashed_data = hmac.new(bytes(hash_key), data.encode('utf-8'))
    return hashed_data.hexdigest()
