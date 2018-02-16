import pytest
from crypt_utils import get_salt, sign_string


@pytest.fixture
def sample_key() -> str:
    return 'sample secret key'


@pytest.fixture
def sample_salt() -> str:
    return 'sample salt'


@pytest.fixture
def sample_data() -> str:
    return 'sample file contents'


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
    assert actual == 'e963d1772884f7107601e10cfe6dfab2'
