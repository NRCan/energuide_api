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


def test_read(sample_fixture: str):
    data = reader.read(sample_fixture)

    expected = [{'EVAL_ID': '123456',
                 'IDNUMBER': '23',
                 'CREATIONDATE': '2009-01-01 12:01:02',
                 'MODIFICATIONDATE': '2011-01-01 00:01:02',
                 'YEARBUILT': '1979',
                 'HOUSEREGION': 'Ontario',
                 'CLIENTCITY': 'Kingston',
                 'CLIENTPCODE': 'K0H 1Y0'},
                {'EVAL_ID': '123457',
                 'IDNUMBER': '24',
                 'CREATIONDATE': '2009-01-02 12:01:02',
                 'MODIFICATIONDATE': '2011-01-02 00:01:02',
                 'YEARBUILT': '1978',
                 'HOUSEREGION': 'Alberta',
                 'CLIENTCITY': 'Kingston',
                 'CLIENTPCODE': 'K0H 1Y1'},
                {'EVAL_ID': '123458',
                 'IDNUMBER': '25',
                 'CREATIONDATE': '2009-01-03 12:01:02',
                 'MODIFICATIONDATE': '2011-01-03 00:01:02',
                 'YEARBUILT': '1980',
                 'HOUSEREGION': 'Québec',
                 'CLIENTCITY': 'Kingston',
                 'CLIENTPCODE': 'K0H 1Y2'}]

    assert list(data) == expected


def test_grouper(sample: typing.List[reader.InputData]) -> None:
    output = list(reader.grouper(sample, _GROUP_KEY))

    assert output[0] == sample[0:2]
    assert output[1] == sample[2:]
