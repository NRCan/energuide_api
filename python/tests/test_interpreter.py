import datetime
import typing
import pytest
from energuide import interpreter

# pylint: disable=no-self-use


@pytest.fixture
def sample_eval_d() -> interpreter.InputData:
    return {
        'EVAL_ID': 123,
        'EVAL_TYPE': 'D',
        'ENTRYDATE': '2018-01-01',
        'CREATIONDATE': '2018-01-08 09:00:00',
        'MODIFICATIONDATE': '2018-06-01 09:00:00',
        'CLIENTCITY': 'Ottawa',
        'CLIENTPCODE': 'K1P 0A6',
        'HOUSEREGION': 'Ontario',
        'YEARBUILT': 2000,
    }


@pytest.fixture
def sample_parsed_d(sample_eval_d: interpreter.InputData) -> interpreter.ParsedDwellingDataRow:
    return interpreter.ParsedDwellingDataRow.from_row(sample_eval_d)  # pylint: disable=no-member


@pytest.fixture
def sample_eval_e() -> interpreter.InputData:
    return {
        'EVAL_ID': 123,
        'EVAL_TYPE': 'E',
        'ENTRYDATE': '2018-02-01',
        'CREATIONDATE': '2018-02-08 09:00:00',
        'MODIFICATIONDATE': '2018-06-01 09:00:00',
        'CLIENTCITY': 'Montreal',
        'CLIENTPCODE': 'G1A 1A3',
        'HOUSEREGION': 'Quebec',
        'YEARBUILT': 2001,
    }


@pytest.fixture
def sample_parsed_e(sample_eval_e: interpreter.InputData) -> interpreter.ParsedDwellingDataRow:
    return interpreter.ParsedDwellingDataRow.from_row(sample_eval_e)


class TestEvaluationType:

    def test_from_code(self):
        code = interpreter.EvaluationType.PRE_RETROFIT.value
        output = interpreter.EvaluationType.from_code(code)
        assert output == interpreter.EvaluationType.PRE_RETROFIT


class TestRegion:

    def test_from_name(self):
        data = [
            'Ontario',
            'british columbia',
            'NOVA SCOTIA',
        ]
        output = [interpreter.Region.from_data(row) for row in data]

        assert output == [
            interpreter.Region.ONTARIO,
            interpreter.Region.BRITISH_COLUMBIA,
            interpreter.Region.NOVA_SCOTIA,
        ]

    def test_from_unknown_name(self):
        assert interpreter.Region.from_data('foo') == interpreter.Region.UNKNOWN

    def test_from_code(self):
        data = [
            'ON',
            'bc',
            'Ns',
        ]
        output = [interpreter.Region.from_data(row) for row in data]
        assert output == [
            interpreter.Region.ONTARIO,
            interpreter.Region.BRITISH_COLUMBIA,
            interpreter.Region.NOVA_SCOTIA,
        ]

    def test_from_unknown_code(self):
        assert interpreter.Region.from_data('CA') == interpreter.Region.UNKNOWN


class TestParsedDwellingDataRow:

    def test_from_row(self, sample_eval_d: interpreter.InputData) -> None:
        output = interpreter.ParsedDwellingDataRow.from_row(sample_eval_d)
        assert output == interpreter.ParsedDwellingDataRow(
            eval_id=123,
            eval_type=interpreter.EvaluationType.PRE_RETROFIT,
            entry_date=datetime.date(2018, 1, 1),
            creation_date=datetime.datetime(2018, 1, 8, 9),
            modification_date=datetime.datetime(2018, 6, 1, 9),
            year_built=2000,
            city='Ottawa',
            region=interpreter.Region.ONTARIO,
            postal_code='K1P 0A6',
            forward_sortation_area='K1P',
        )

    def test_bad_postal_code(self, sample_eval_d: interpreter.InputData) -> None:
        sample_eval_d['CLIENTPCODE'] = 'K1P 016'
        with pytest.raises(interpreter.InvalidInputDataException):
            interpreter.ParsedDwellingDataRow.from_row(sample_eval_d)

    def test_from_bad_row(self) -> None:
        input_data = {
            'EVAL_ID': 123
        }
        with pytest.raises(interpreter.InvalidInputDataException) as ex:
            interpreter.ParsedDwellingDataRow.from_row(input_data)
        assert 'EVAL_TYPE' in ex.exconly()
        assert 'EVAL_ID' not in ex.exconly()


def test_read(energuide_fixture: str):
    data = interpreter.read(energuide_fixture)

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


@pytest.fixture
def chunked_data() -> typing.Iterator[typing.List[interpreter.InputData]]:
    return iter([[{'EVAL_ID': 123456,
                   'IDNUMBER': '23',
                   'EVAL_TYPE': 'E',
                   'CREATIONDATE': '2009-01-01 12:00:00',
                   'MODIFICATIONDATE': '2011-01-01 00:00:00',
                   'ENTRYDATE': '2018-02-01',
                   'YEARBUILT': 1979,
                   'HOUSEREGION': 'Ontario',
                   'CLIENTCITY': 'Kingston',
                   'CLIENTPCODE': 'K0H 1Y0'},
                  {'EVAL_ID': 123457,
                   'IDNUMBER': '24',
                   'EVAL_TYPE': 'E',
                   'CREATIONDATE': '2009-01-02 12:00:00',
                   'MODIFICATIONDATE': '2011-01-02 00:00:00',
                   'ENTRYDATE': '2018-02-01',
                   'YEARBUILT': 1978,
                   'HOUSEREGION': 'Alberta',
                   'CLIENTCITY': 'Kingston',
                   'CLIENTPCODE': 'K0H 1Y1'},
                  {'EVAL_ID': 123458,
                   'IDNUMBER': '25',
                   'EVAL_TYPE': 'E',
                   'CREATIONDATE': '2009-01-03 12:00:00',
                   'MODIFICATIONDATE': '2011-01-03 00:00:00',
                   'ENTRYDATE': '2018-02-01',
                   'YEARBUILT': 1980,
                   'HOUSEREGION': 'Quebec',
                   'CLIENTCITY': 'Kingston',
                   'CLIENTPCODE': 'K0H 1Y2'}]])


def test_parse(chunked_data: typing.Iterator[typing.List[interpreter.InputData]]) -> None:
    print(chunked_data)
    parsed = interpreter.parse(chunked_data)

    expected = [interpreter.ParsedDwellingDataRow(
        eval_id=123456,
        eval_type=interpreter.EvaluationType.POST_RETROFIT,
        entry_date=datetime.date(2018, 2, 1),
        creation_date=datetime.datetime(2009, 1, 1, 12),
        modification_date=datetime.datetime(2011, 1, 1, 0),
        year_built=1979,
        city='Kingston',
        region=interpreter.Region.ONTARIO,
        postal_code='K0H 1Y0',
        forward_sortation_area='K0H',
        ), interpreter.ParsedDwellingDataRow(
            eval_id=123457,
            eval_type=interpreter.EvaluationType.POST_RETROFIT,
            entry_date=datetime.date(2018, 2, 1),
            creation_date=datetime.datetime(2009, 1, 2, 12),
            modification_date=datetime.datetime(2011, 1, 2, 0),
            year_built=1978,
            city='Kingston',
            region=interpreter.Region.ALBERTA,
            postal_code='K0H 1Y1',
            forward_sortation_area='K0H',
        ), interpreter.ParsedDwellingDataRow(
            eval_id=123458,
            eval_type=interpreter.EvaluationType.POST_RETROFIT,
            entry_date=datetime.date(2018, 2, 1),
            creation_date=datetime.datetime(2009, 1, 3, 12),
            modification_date=datetime.datetime(2011, 1, 3, 0),
            year_built=1980,
            city='Kingston',
            region=interpreter.Region.QUEBEC,
            postal_code='K0H 1Y2',
            forward_sortation_area='K0H',
        )]

    assert list(parsed)[0] == expected
