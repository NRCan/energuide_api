import datetime
import typing
import pytest
from energuide import dwelling

# pylint: disable=no-self-use


@pytest.fixture
def sample_eval_d() -> dwelling.EvaluationData:
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
def sample_parsed_d(sample_eval_d: dwelling.EvaluationData) -> dwelling.ParsedDwellingDataRow:
    return dwelling.ParsedDwellingDataRow.from_row(sample_eval_d)  # pylint: disable=no-member


@pytest.fixture
def sample_eval_e() -> dwelling.EvaluationData:
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
def sample_parsed_e(sample_eval_e: dwelling.EvaluationData) -> dwelling.ParsedDwellingDataRow:
    return dwelling.ParsedDwellingDataRow.from_row(sample_eval_e)


class TestEvaluationType:

    def test_from_code(self):
        code = dwelling.EvaluationType.PRE_RETROFIT.value
        output = dwelling.EvaluationType.from_code(code)
        assert output == dwelling.EvaluationType.PRE_RETROFIT


class TestRegion:

    def test_from_name(self):
        data = [
            'Ontario',
            'british columbia',
            'NOVA SCOTIA',
        ]
        output = [dwelling.Region.from_data(row) for row in data]

        assert output == [
            dwelling.Region.ONTARIO,
            dwelling.Region.BRITISH_COLUMBIA,
            dwelling.Region.NOVA_SCOTIA,
        ]

    def test_from_unknown_name(self):
        assert dwelling.Region.from_data('foo') == dwelling.Region.UNKNOWN

    def test_from_code(self):
        data = [
            'ON',
            'bc',
            'Ns',
        ]
        output = [dwelling.Region.from_data(row) for row in data]
        assert output == [
            dwelling.Region.ONTARIO,
            dwelling.Region.BRITISH_COLUMBIA,
            dwelling.Region.NOVA_SCOTIA,
        ]

    def test_from_unknown_code(self):
        assert dwelling.Region.from_data('CA') == dwelling.Region.UNKNOWN


class TestParsedDwellingDataRow:

    def test_from_row(self, sample_eval_d: dwelling.EvaluationData) -> None:
        output = dwelling.ParsedDwellingDataRow.from_row(sample_eval_d)
        assert output == dwelling.ParsedDwellingDataRow(
            eval_id=123,
            eval_type=dwelling.EvaluationType.PRE_RETROFIT,
            entry_date=datetime.date(2018, 1, 1),
            creation_date=datetime.datetime(2018, 1, 8, 9),
            modification_date=datetime.datetime(2018, 6, 1, 9),
            year_built=2000,
            city='Ottawa',
            region=dwelling.Region.ONTARIO,
            postal_code='K1P 0A6',
            forward_sortation_area='K1P',
        )

    def test_bad_postal_code(self, sample_eval_d: dwelling.EvaluationData) -> None:
        sample_eval_d['CLIENTPCODE'] = 'K1P 016'
        with pytest.raises(dwelling.InvalidInputDataException):
            dwelling.ParsedDwellingDataRow.from_row(sample_eval_d)

    def test_from_bad_row(self) -> None:
        input_data = {
            'EVAL_ID': 123
        }
        with pytest.raises(dwelling.InvalidInputDataException) as ex:
            dwelling.ParsedDwellingDataRow.from_row(input_data)
        assert 'EVAL_TYPE' in ex.exconly()
        assert 'EVAL_ID' not in ex.exconly()


class TestDwellingEvaluation:

    def test_eval_type(self, sample_parsed_d: dwelling.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d)
        assert output.evaluation_type == dwelling.EvaluationType.PRE_RETROFIT

    def test_entry_date(self, sample_parsed_d: dwelling.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d)
        assert output.entry_date == datetime.date(2018, 1, 1)

    def test_creation_date(self, sample_parsed_d: dwelling.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d)
        assert output.creation_date == datetime.datetime(2018, 1, 8, 9)

    def test_modification_date(self, sample_parsed_d: dwelling.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d)
        assert output.modification_date == datetime.datetime(2018, 6, 1, 9)

    def test_to_dict(self, sample_parsed_d: dwelling.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d).to_dict()
        assert output['evaluationType'] == 'PRE_RETROFIT'


class TestDwelling:

    @pytest.fixture
    def sample(self,
               sample_parsed_d: dwelling.ParsedDwellingDataRow,
               sample_parsed_e: dwelling.ParsedDwellingDataRow,
              ) -> typing.List[dwelling.ParsedDwellingDataRow]:
        return [sample_parsed_d, sample_parsed_e]

    def test_house_id(self, sample: typing.List[dwelling.ParsedDwellingDataRow]) -> None:
        output = dwelling.Dwelling.from_data(sample)
        assert output.house_id == 123

    def test_year_built(self, sample: typing.List[dwelling.ParsedDwellingDataRow]) -> None:
        output = dwelling.Dwelling.from_data(sample)
        assert output.year_built == 2000

    def test_address_data(self, sample: typing.List[dwelling.ParsedDwellingDataRow]) -> None:
        output = dwelling.Dwelling.from_data(sample)
        assert output.city == 'Ottawa'
        assert output.region == dwelling.Region.ONTARIO
        assert output.postal_code == 'K1P 0A6'
        assert output.forward_sortation_area == 'K1P'

    def test_evaluations(self, sample: typing.List[dwelling.ParsedDwellingDataRow]) -> None:
        output = dwelling.Dwelling.from_data(sample)
        assert len(output.evaluations) == 2

    def test_no_data(self) -> None:
        data: typing.List[typing.Any] = []
        with pytest.raises(dwelling.NoInputDataException):
            dwelling.Dwelling.from_data(data)

    def test_to_dict(self, sample: typing.List[dwelling.ParsedDwellingDataRow]) -> None:
        output = dwelling.Dwelling.from_data(sample).to_dict()
        assert output['houseId'] == 123
        assert len(output['evaluations']) == 2
        assert 'postalCode' not in output
