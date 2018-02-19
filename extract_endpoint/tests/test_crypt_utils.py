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


def test_sign_string(sample_salt: str, sample_key: str, sample_data: str) -> None:
    actual = sign_string(salt=sample_salt, key=sample_key, data=sample_data)
    assert actual == '8a2dbe236ead75dd242d3ee015b3d8b6'


def test_sign_string_no_salt(sample_key: str, sample_data: str) -> None:
    actual = sign_string(salt=None, key=sample_key, data=sample_data)
    assert actual == '188119f4319b02e76b50d297acc5b9cd'
