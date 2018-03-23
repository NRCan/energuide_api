import copy
import datetime
import typing
import pytest
from energuide import dwelling
from energuide.embedded import upgrade
from energuide.embedded import measurement
from energuide.exceptions import InvalidInputDataError
from energuide.exceptions import InvalidGroupSizeError


# pylint: disable=no-self-use


@pytest.fixture
def upgrades_input() -> typing.List[str]:
    return [
        '<Ceilings cost="0" priority="12" />',
        '<MainWalls cost="1" priority="2" />',
        '<Foundation cost="2" priority="3" />',
        ]


@pytest.fixture
def sample_input_d(upgrades_input: typing.List[str]) -> typing.Dict[str, typing.Any]:

    return {
        'HOUSE_ID': '456',
        'EVAL_ID': '123',
        'EVAL_TYPE': 'D',
        'ENTRYDATE': '2018-01-01',
        'CREATIONDATE': '2018-01-08 09:00:00',
        'MODIFICATIONDATE': '2018-06-01 09:00:00',
        'CLIENTCITY': 'Ottawa',
        'forwardSortationArea': 'K1P',
        'HOUSEREGION': 'Ontario',
        'YEARBUILT': '2000',
        'BUILDER': '4K13D01404',
        'HEATEDFLOORAREA': None,
        'TYPEOFHOUSE': 'Single detached',
        'ERSRATING': '567',
        'UGRERSRATING': '565',
        'ERSGHG': None,
        'UGRERSGHG': None,
        'upgrades': upgrades_input,
        'ERSENERGYINTENSITY': '0.82',
        'UGRERSENERGYINTENSITY': '0.80',
        'EGHRATING': '50',
        'UGRRATING': '49',

        'WALLDEF': '45.3;12;50;12;4.7;12',
        'UGRWALLDEF': '45.3;12;50;12;4.7;10',
        'EGHHLWALLS': '27799.9',
        'UGRHLWALLS': '27799.9',
    }


@pytest.fixture
def sample_input_e(sample_input_d: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    output = copy.deepcopy(sample_input_d)
    output['EVAL_TYPE'] = 'E'
    output['ENTRYDATE'] = '2018-01-02'
    return output


@pytest.fixture
def sample_input_missing(sample_input_d: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    output = copy.deepcopy(sample_input_d)
    output['MODIFICATIONDATE'] = None
    output['ERSRATING'] = None
    output['UGRERSRATING'] = None
    return output


@pytest.fixture
def sample_parsed_d(sample_input_d: typing.Dict[str, typing.Any]) -> dwelling.ParsedDwellingDataRow:
    return dwelling.ParsedDwellingDataRow.from_row(sample_input_d)


@pytest.fixture
def sample_parsed_e(sample_input_e: typing.Dict[str, typing.Any]) -> dwelling.ParsedDwellingDataRow:
    return dwelling.ParsedDwellingDataRow.from_row(sample_input_e)


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

    def test_from_row(self, sample_input_d: typing.Dict[str, typing.Any]) -> None:
        output = dwelling.ParsedDwellingDataRow.from_row(sample_input_d)

        assert output == dwelling.ParsedDwellingDataRow(
            house_id=456,
            eval_id=123,
            file_id='4K13D01404',
            eval_type=dwelling.EvaluationType.PRE_RETROFIT,
            entry_date=datetime.date(2018, 1, 1),
            creation_date=datetime.datetime(2018, 1, 8, 9),
            modification_date=datetime.datetime(2018, 6, 1, 9),
            year_built=2000,
            city='Ottawa',
            region=dwelling.Region.ONTARIO,
            forward_sortation_area='K1P',
            energy_upgrades=[
                upgrade.Upgrade(
                    upgrade_type='Ceilings',
                    cost=0,
                    priority=12,
                ),
                upgrade.Upgrade(
                    upgrade_type='MainWalls',
                    cost=1,
                    priority=2,
                ),
                upgrade.Upgrade(
                    upgrade_type='Foundation',
                    cost=2,
                    priority=3,
                ),
            ],
            house_type='Single detached',
            heated_floor_area=None,
            egh_rating=measurement.Measurement(
                measurement=50,
                upgrade=49,
            ),
            ers_rating=measurement.Measurement(
                measurement=567,
                upgrade=565,
            ),
            greenhouse_gas_emissions=measurement.Measurement(
                measurement=None,
                upgrade=None,
            ),
            energy_intensity=measurement.Measurement(
                measurement=0.82,
                upgrade=0.80,
            ),
            walls=measurement.Measurement(
                measurement={
                    'insulation': [
                        {
                            'percentage': 45.3,
                            'rValue': 12.0,
                        }, {
                            'percentage': 50.0,
                            'rValue': 12.0,
                        }, {
                            'percentage': 4.7,
                            'rValue': 12.0,
                        }
                    ],
                    'heatLost': 27799.9
                },
                upgrade={
                    'insulation': [
                        {
                            'percentage': 45.3,
                            'rValue': 12.0,
                        }, {
                            'percentage': 50.0,
                            'rValue': 12.0,
                        }, {
                            'percentage': 4.7,
                            'rValue': 10.0,
                        }
                    ],
                    'heatLost': 27799.9
                },
            )
        )

    def test_null_fields_are_accepted(self, sample_input_missing: typing.Dict[str, typing.Any]) -> None:
        output = dwelling.ParsedDwellingDataRow.from_row(sample_input_missing)

        assert output.modification_date is None
        assert output.ers_rating == measurement.Measurement(None, None)

    def test_bad_postal_code(self, sample_input_d: typing.Dict[str, typing.Any]) -> None:
        sample_input_d['forwardSortationArea'] = 'K16'
        with pytest.raises(InvalidInputDataError):
            dwelling.ParsedDwellingDataRow.from_row(sample_input_d)

    def test_from_bad_row(self) -> None:
        input_data = {
            'EVAL_ID': 123
        }
        with pytest.raises(InvalidInputDataError) as ex:
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
        assert output['evaluationType'] == dwelling.EvaluationType.PRE_RETROFIT.value


class TestDwelling:

    @pytest.fixture
    def sample(self,
               sample_input_d: typing.Dict[str, typing.Any],
               sample_input_e: typing.Dict[str, typing.Any],
              ) -> typing.List[typing.Dict[str, typing.Any]]:
        return [sample_input_d, sample_input_e].copy()

    def test_house_id(self, sample: typing.List[typing.Dict[str, typing.Any]]) -> None:
        output = dwelling.Dwelling.from_group(sample)
        assert output.house_id == 456

    def test_year_built(self, sample: typing.List[typing.Dict[str, typing.Any]]) -> None:
        output = dwelling.Dwelling.from_group(sample)
        assert output.year_built == 2000

    def test_address_data(self, sample: typing.List[typing.Dict[str, typing.Any]]) -> None:
        output = dwelling.Dwelling.from_group(sample)
        assert output.city == 'Ottawa'
        assert output.region == dwelling.Region.ONTARIO
        assert output.forward_sortation_area == 'K1P'

    def test_evaluations(self, sample: typing.List[typing.Dict[str, typing.Any]]) -> None:
        output = dwelling.Dwelling.from_group(sample)
        assert len(output.evaluations) == 2

    def test_no_data(self) -> None:
        data: typing.List[typing.Any] = []
        with pytest.raises(InvalidGroupSizeError):
            dwelling.Dwelling.from_group(data)

    def test_to_dict(self, sample: typing.List[typing.Dict[str, typing.Any]]) -> None:
        output = dwelling.Dwelling.from_group(sample).to_dict()
        assert output['houseId'] == 456
        assert len(output['evaluations']) == 2
        assert 'postalCode' not in output
        assert output['region'] == dwelling.Region.ONTARIO.value
