import typing
import pytest
from energuide import dwelling


@pytest.fixture
def sample() -> dwelling.DwellingData:
    return [
        {
            'EVAL_ID': 123,
        }, {
            'EVAL_ID': 123,
        }
    ]


def test_house_id(sample: dwelling.DwellingData) -> None:
    output = dwelling.Dwelling.from_data(sample)
    assert output.house_id == 123


def test_no_data() -> None:
    data: typing.List[typing.Any] = []
    with pytest.raises(dwelling.NoInputDataException):
        dwelling.Dwelling.from_data(data)


def test_bad_data() -> None:
    data = [{'foo': 123}]
    with pytest.raises(dwelling.InvalidInputDataException):
        dwelling.Dwelling.from_data(data)
