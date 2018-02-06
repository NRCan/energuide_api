import typing
import pytest
from energuide import reader
from energuide import extracted_datatypes


# pylint: disable=no-self-use


@pytest.fixture
def ceiling_input() -> typing.Dict[str, str]:
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
def floor_input() -> typing.Dict[str, str]:
    return {
        'label': 'Rm over garage',
        'nominalRsi': '2.46',
        'effectiveRsi': '2.9181',
        'area': '9.2903',
        'length': '3.048',
    }


@pytest.fixture
def wall_input() -> typing.Dict[str, str]:
    return {
        'label': 'Second level',
        'constructionTypeCode': 'Code 1',
        'constructionTypeValue': '1201101121',
        'nominalRsi': '1.432',
        'effectiveRsi': '1.8016',
        'perimeter': '42.9768',
        'height': '2.4384',
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
            }
        ]
    }


@pytest.fixture
def codes(raw_codes: typing.Dict[str, typing.List[typing.Dict[str, str]]]) -> extracted_datatypes.Codes:
    return extracted_datatypes.Codes.from_data(raw_codes)



@pytest.fixture
def sample_input_d(ceiling_input: reader.InputData,
                   floor_input: reader.InputData,
                   wall_input,
                   raw_codes,) -> reader.InputData:
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
        'walls': [
            wall_input
        ],
        'codes': raw_codes

    }

class TestWallCode:

    @pytest.fixture
    def sample(self, raw_codes: typing.Dict[str, typing.List[typing.Dict[str, str]]]) -> typing.Dict[str, str]:
        return raw_codes['wall'][0]

    def test_from_data(self, sample: typing.Dict[str, str]) -> None:
        output = extracted_datatypes.WallCode.from_data(sample)
        assert output.id == 'Code 1'
        assert output.label == '1201101121'


class TestCodes:

    def test_from_data(self, raw_codes: typing.Dict[str, typing.List[typing.Dict[str, str]]]):
        output = extracted_datatypes.Codes.from_data(raw_codes)
        assert len(output.wall) == 1
        assert output.wall['Code 1'].id == 'Code 1'


class TestCeiling:

    @pytest.fixture
    def sample(self, ceiling_input: reader.InputData) -> typing.Dict[str, typing.Any]:
        ceiling = ceiling_input.copy()
        ceiling['nominalRsi'] = float(ceiling['nominalRsi'])
        ceiling['effectiveRsi'] = float(ceiling['effectiveRsi'])
        ceiling['area'] = float(ceiling['area'])
        ceiling['length'] = float(ceiling['length'])
        return ceiling

    def test_from_data(self, sample: typing.Dict[str, typing.Any]) -> None:
        output = extracted_datatypes.Ceiling.from_data(sample)
        assert output.label == 'Main attic'
        assert output.area_metres == 46.4515

    def test_to_dict(self, sample: typing.Dict[str, typing.Any]) -> None:
        output = extracted_datatypes.Ceiling.from_data(sample).to_dict()
        assert output['areaMetres'] == sample['area']


class TestFloor:

    @pytest.fixture
    def sample(self, floor_input: typing.Dict[str, str]) -> typing.Dict[str, typing.Any]:
        floor = floor_input.copy()
        floor['nominalRsi'] = float(floor['nominalRsi'])
        floor['effectiveRsi'] = float(floor['effectiveRsi'])
        floor['area'] = float(floor['area'])
        floor['length'] = float(floor['length'])
        return floor

    def test_from_data(self, sample: typing.Dict[str, typing.Any]) -> None:
        output = extracted_datatypes.Floor.from_data(sample)
        assert output.label == 'Rm over garage'
        assert output.area_metres == 9.2903

    def test_to_dict(self, sample: typing.Dict[str, typing.Any]) -> None:
        output = extracted_datatypes.Floor.from_data(sample).to_dict()
        assert output['areaMetres'] == sample['area']


class TestWall:

    @pytest.fixture
    def sample(self, wall_input: typing.Dict[str, str]) -> typing.Dict[str, typing.Any]:
        wall = wall_input.copy()
        wall['nominalRsi'] = float(wall['nominalRsi'])
        wall['effectiveRsi'] = float(wall['effectiveRsi'])
        wall['perimeter'] = float(wall['perimeter'])
        wall['height'] = float(wall['height'])
        return wall

    def test_from_data(self,
                       sample: typing.Dict[str, typing.Any],
                       codes: extracted_datatypes.Codes) -> None:
        output = extracted_datatypes.Wall.from_data(sample, codes.wall)
        assert output.label == 'Second level'
        assert output.perimeter == 42.9768
        assert output.component_type_size_english == '38x89 mm (2x4 in)'

    def test_missing_optional_fields(self,
                                     sample: typing.Dict[str, typing.Any],
                                     codes: extracted_datatypes.Codes) -> None:
        wall = sample.copy()
        wall.pop('constructionTypeCode')
        wall.pop('constructionTypeValue')
        output = extracted_datatypes.Wall.from_data(wall, codes.wall)
        assert output.label == 'Second level'
        assert output.perimeter == 42.9768
        assert output.component_type_size_english is None

    def test_to_dict(self,
                     sample: typing.Dict[str, typing.Any],
                     codes: extracted_datatypes.Codes) -> None:
        output = extracted_datatypes.Wall.from_data(sample, codes.wall).to_dict()
        assert output['areaMetres'] == sample['perimeter'] * sample['height']
