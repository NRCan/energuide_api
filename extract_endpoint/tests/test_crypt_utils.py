import pytest
from crypt_utils import get_salt, sign_string


@pytest.fixture
def sample_key() -> str:
    return 'sample key'


@pytest.fixture
def sample_salt() -> str:
    return 'sample salt'


@pytest.fixture
def sample_data() -> str:
    return 'sample data'


def test_get_salt() -> None:
    salt_1 = get_salt()
    salt_2 = get_salt()
    assert len(salt_1) == 88
    assert salt_1 != salt_2


def test_get_salt_small() -> None:
    salt_1 = get_salt(1)
    assert len(salt_1) == 4


def test_sign_string(sample_salt: str, sample_key: str, sample_data: str) -> None:
    actual = sign_string(salt=sample_salt, key=sample_key, data=sample_data)
    assert actual == '8a2dbe236ead75dd242d3ee015b3d8b6'
