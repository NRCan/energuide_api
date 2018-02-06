import datetime
import typing
import pytest
from energuide import dwelling
from energuide import reader
from energuide import extracted_datatypes


# pylint: disable=no-self-use

@pytest.fixture
def ceiling_input() -> reader.InputData:
    return {
        'label': 'Main attic',
        'typeEnglish': 'Attic/gable',
        'typeFrench': 'Combles/pignon',
        'nominalRsi': '2.864',
        'effectiveRsi': '2.9463',
        'area': '46.4515',
        'length': '23.875',
    }


@pytest.fixture
def floor_input() -> reader.InputData:
    return {
        'label': 'Rm over garage',
        'nominalRsi': '2.46',
        'effectiveRsi': '2.9181',
        'area': '9.2903',
        'length': '3.048',
    }


@pytest.fixture
def raw_codes() -> typing.Dict[str, typing.List[typing.Dict[str, str]]]:
    return {
        'wall': [
            {
                'id': 'Code 1',
                'label': '1201101121',
                'structureTypeEnglish': 'Wood frame',
                'structureTypeFrench': 'Ossature de bois',
                'componentTypeSizeEnglish': '38x89 mm (2x4 in)',
                'componentTypeSizeFrench': '38x89 (2x4)',
            }, {
                'id': 'Code 2',
                'label': '1201101122',
                'structureTypeEnglish': 'Metal frame',
                'structureTypeFrench': 'Ossature de métal',
                'componentTypeSizeEnglish': '38x89 mm (2x4 in)',
                'componentTypeSizeFrench': '38x89 (2x4)',
            }
        ]
    }


@pytest.fixture
def sample_input_d(ceiling_input: reader.InputData,
                   floor_input: reader.InputData,
                   raw_codes: typing.Dict[str, typing.List[typing.Dict[str, str]]]) -> reader.InputData:
    return {
        'EVAL_ID': '123',
        'EVAL_TYPE': 'D',
        'ENTRYDATE': '2018-01-01',
        'CREATIONDATE': '2018-01-08 09:00:00',
        'MODIFICATIONDATE': '2018-06-01 09:00:00',
        'CLIENTCITY': 'Ottawa',
        'forwardSortationArea': 'K1P',
        'HOUSEREGION': 'Ontario',
        'YEARBUILT': '2000',
        'ceilings': [
            ceiling_input
        ],
        'floors': [
            floor_input
        ],
        'codes': raw_codes
    }


@pytest.fixture
def sample_input_e(sample_input_d: reader.InputData) -> reader.InputData:
    output = sample_input_d.copy()
    output['EVAL_TYPE'] = 'E'
    return output


@pytest.fixture
def sample_parsed_d(sample_input_d: reader.InputData) -> dwelling.ParsedDwellingDataRow:
    return dwelling.ParsedDwellingDataRow.from_row(sample_input_d)


@pytest.fixture
def sample_parsed_e(sample_input_e: reader.InputData) -> dwelling.ParsedDwellingDataRow:
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

    def test_from_row(self, sample_input_d: reader.InputData) -> None:
        output = dwelling.ParsedDwellingDataRow.from_row(sample_input_d)
        assert output == dwelling.ParsedDwellingDataRow(
            eval_id=123,
            eval_type=dwelling.EvaluationType.PRE_RETROFIT,
            entry_date=datetime.date(2018, 1, 1),
            creation_date=datetime.datetime(2018, 1, 8, 9),
            modification_date=datetime.datetime(2018, 6, 1, 9),
            year_built=2000,
            city='Ottawa',
            region=dwelling.Region.ONTARIO,
            forward_sortation_area='K1P',
            ceilings=[
                extracted_datatypes.Ceiling(
                    label='Main attic',
                    type_english='Attic/gable',
                    type_french='Combles/pignon',
                    nominal_rsi=2.864,
                    effective_rsi=2.9463,
                    area_metres=46.4515,
                    length_metres=23.875
                )
            ],
            floors=[
                extracted_datatypes.Floor(
                    label='Rm over garage',
                    nominal_rsi=2.46,
                    effective_rsi=2.9181,
                    area_metres=9.2903,
                    length_metres=3.048,
                )
            ]
        )

    def test_bad_postal_code(self, sample_input_d: reader.InputData) -> None:
        sample_input_d['forwardSortationArea'] = 'K16'
        with pytest.raises(reader.InvalidInputDataException):
            dwelling.ParsedDwellingDataRow.from_row(sample_input_d)

    def test_from_bad_row(self) -> None:
        input_data = {
            'EVAL_ID': 123
        }
        with pytest.raises(reader.InvalidInputDataException) as ex:
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
               sample_input_d: reader.InputData,
               sample_input_e: reader.InputData,
              ) -> typing.List[reader.InputData]:
        return [sample_input_d, sample_input_e]

    def test_house_id(self, sample: typing.List[reader.InputData]) -> None:
        output = dwelling.Dwelling.from_group(sample)
        assert output.house_id == 123

    def test_year_built(self, sample: typing.List[reader.InputData]) -> None:
        output = dwelling.Dwelling.from_group(sample)
        assert output.year_built == 2000

    def test_address_data(self, sample: typing.List[reader.InputData]) -> None:
        output = dwelling.Dwelling.from_group(sample)
        assert output.city == 'Ottawa'
        assert output.region == dwelling.Region.ONTARIO
        assert output.forward_sortation_area == 'K1P'

    def test_evaluations(self, sample: typing.List[reader.InputData]) -> None:
        output = dwelling.Dwelling.from_group(sample)
        assert len(output.evaluations) == 2

    def test_no_data(self) -> None:
        data: typing.List[typing.Any] = []
        with pytest.raises(dwelling.NoInputDataException):
            dwelling.Dwelling.from_group(data)

    def test_to_dict(self, sample: typing.List[reader.InputData]) -> None:
        output = dwelling.Dwelling.from_group(sample).to_dict()
        assert output['houseId'] == 123
        assert len(output['evaluations']) == 2
        assert 'postalCode' not in output
        assert output['region'] == dwelling.Region.ONTARIO.value
