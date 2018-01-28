import datetime
import typing
import pytest
from energuide import dwelling, interpreter

# pylint: disable=no-self-use


@pytest.fixture
def sample_parsed_d() -> interpreter.ParsedDwellingDataRow:
    return interpreter.ParsedDwellingDataRow(
        eval_id=123,
        eval_type=interpreter.EvaluationType.PRE_RETROFIT,
        entry_date=datetime.date(2018, 1, 1),
        creation_date=datetime.datetime(2018, 1, 8, 9),
        modification_date=datetime.datetime(2018, 6, 1, 9),
        city='Ottawa',
        region=interpreter.Region.ONTARIO,
        postal_code='K1P 0A6',
        forward_sortation_area='K1P',
        year_built=2000
    )


@pytest.fixture
def sample_parsed_e() -> interpreter.ParsedDwellingDataRow:
    return interpreter.ParsedDwellingDataRow(
        eval_id=123,
        eval_type=interpreter.EvaluationType.POST_RETROFIT,
        entry_date=datetime.date(2018, 2, 1),
        creation_date=datetime.datetime(2018, 2, 8, 9),
        modification_date=datetime.datetime(2018, 6, 1, 9),
        city='Montreal',
        region=interpreter.Region.QUEBEC,
        postal_code='G1A 1A3',
        forward_sortation_area='G1A',
        year_built=2001,
    )


class TestDwellingEvaluation:

    def test_eval_type(self, sample_parsed_d: interpreter.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d)
        assert output.evaluation_type == interpreter.EvaluationType.PRE_RETROFIT

    def test_entry_date(self, sample_parsed_d: interpreter.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d)
        assert output.entry_date == datetime.date(2018, 1, 1)

    def test_creation_date(self, sample_parsed_d: interpreter.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d)
        assert output.creation_date == datetime.datetime(2018, 1, 8, 9)

    def test_modification_date(self, sample_parsed_d: interpreter.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d)
        assert output.modification_date == datetime.datetime(2018, 6, 1, 9)

    def test_to_dict(self, sample_parsed_d: interpreter.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d).to_dict()
        assert output['evaluationType'] == interpreter.EvaluationType.PRE_RETROFIT


class TestDwelling:

    @pytest.fixture
    def sample(self,
               sample_parsed_d: interpreter.ParsedDwellingDataRow,
               sample_parsed_e: interpreter.ParsedDwellingDataRow,
              ) -> typing.List[interpreter.ParsedDwellingDataRow]:
        return [sample_parsed_d, sample_parsed_e]

    def test_house_id(self, sample: typing.List[interpreter.ParsedDwellingDataRow]) -> None:
        output = dwelling.Dwelling.from_data(sample)
        assert output.house_id == 123

    def test_year_built(self, sample: typing.List[interpreter.ParsedDwellingDataRow]) -> None:
        output = dwelling.Dwelling.from_data(sample)
        assert output.year_built == 2000

    def test_address_data(self, sample: typing.List[interpreter.ParsedDwellingDataRow]) -> None:
        output = dwelling.Dwelling.from_data(sample)
        assert output.city == 'Ottawa'
        assert output.region == interpreter.Region.ONTARIO
        assert output.postal_code == 'K1P 0A6'
        assert output.forward_sortation_area == 'K1P'

    def test_evaluations(self, sample: typing.List[interpreter.ParsedDwellingDataRow]) -> None:
        output = dwelling.Dwelling.from_data(sample)
        assert len(output.evaluations) == 2

    def test_no_data(self) -> None:
        data: typing.List[typing.Any] = []
        with pytest.raises(dwelling.NoInputDataException):
            dwelling.Dwelling.from_data(data)

    def test_to_dict(self, sample: typing.List[interpreter.ParsedDwellingDataRow]) -> None:
        output = dwelling.Dwelling.from_data(sample).to_dict()
        assert output['houseId'] == 123
        assert len(output['evaluations']) == 2
        assert 'postalCode' not in output
