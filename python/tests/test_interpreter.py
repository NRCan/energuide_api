import datetime
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
