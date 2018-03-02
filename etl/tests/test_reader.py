import typing
import pytest
from energuide import reader

_GROUP_KEY = 'EVAL_ID'

@pytest.fixture
def sample() -> typing.List[reader.InputData]:
    return [
        {
            _GROUP_KEY: 1,
            'data': 'foo',
        }, {
            _GROUP_KEY: 1,
            'data': 'bar',
        }, {
            _GROUP_KEY: 2,
            'data': 'baz',
        }
    ]


def test_grouper(sample: typing.List[reader.InputData]) -> None:
    output = list(reader.grouper(sample, _GROUP_KEY))

    assert output[0] == sample[0:2]
    assert output[1] == sample[2:]


def test_read(energuide_zip_fixture: str) -> None:
    output = list(reader.read(energuide_zip_fixture))
    assert len(output) == 14


@pytest.mark.usefixtures('skip_if_azure_simulator_not_running', 'put_sample_files_in_azure')
def test_read_from_azure() -> None:
    output = list(reader.read_from_azure())
    assert len(output) == 14
