import hmac


def sign_string(data: str, key: str, salt='') -> str:
    hash_key = (salt + key).encode('utf-8')
    hashed_data = hmac.new(bytes(hash_key), data.encode('utf-8'))
    return hashed_data.hexdigest()
