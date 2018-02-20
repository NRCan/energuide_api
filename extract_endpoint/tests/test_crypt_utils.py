import pytest
from crypt_utils import sign_string


@pytest.fixture
def sample_key() -> str:
    return 'sample key'


@pytest.fixture
def sample_salt() -> str:
    return 'sample salt'


@pytest.fixture
def sample_data() -> str:
    return 'sample data'


def test_sign_string(sample_data: str, sample_key: str, sample_salt: str) -> None:
    actual = sign_string(data=sample_data, key=sample_key, salt=sample_salt)
    assert isinstance(actual, str) and len(actual) == 32


def test_sign_string_no_salt(sample_data: str, sample_key: str) -> None:
    actual = sign_string(data=sample_data, key=sample_key)
    assert isinstance(actual, str) and len(actual) == 32


def test_sign_string_different_salts(sample_data: str, sample_key: str) -> None:
    sig1 = sign_string(data=sample_data, key=sample_key, salt='salt1')
    sig2 = sign_string(data=sample_data, key=sample_key, salt='salt2')
    assert sig1 != sig2


def test_sign_string_different_keys(sample_data: str, sample_salt: str) -> None:
    sig1 = sign_string(data=sample_data, key='key1', salt=sample_salt)
    sig2 = sign_string(data=sample_data, key='key2', salt=sample_salt)
    assert sig1 != sig2
