import typing
import pytest
from energuide import extracted_datatypes


# pylint: disable=no-self-use


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
def codes(raw_codes: typing.Dict[str, typing.List[typing.Dict[str, str]]]) -> extracted_datatypes.Codes:
    return extracted_datatypes.Codes.from_data(raw_codes)


class TestWallCode:

    @pytest.fixture
    def sample(self, raw_codes: typing.Dict[str, typing.List[typing.Dict[str, str]]]) -> typing.Dict[str, str]:
        return raw_codes['wall'][0]

    def test_from_data(self, sample: typing.Dict[str, str]) -> None:
        output = extracted_datatypes.WallCode.from_data(sample)
        assert output.identifier == 'Code 1'
        assert output.label == '1201101121'


class TestCodes:

    def test_from_data(self, raw_codes: typing.Dict[str, typing.List[typing.Dict[str, str]]]) -> None:
        output = extracted_datatypes.Codes.from_data(raw_codes)
        assert len(output.wall) == 2
        assert output.wall['Code 1'].structure_type_english == 'Wood frame'


class TestWall:

    @pytest.fixture
    def sample(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': 'Second level',
            'constructionTypeCode': 'Code 1',
            'constructionTypeValue': '1201101121',
            'nominalRsi': 1.432,
            'effectiveRsi': 1.8016,
            'perimeter': 42.9768,
            'height': 2.4384,
        }

    def test_from_data(self, sample, codes) -> None:
        output = extracted_datatypes.Wall.from_data(sample, codes.wall)
        assert output.label == 'Second level'
        assert output.perimeter == 42.9768

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


class TestCeiling:

    @pytest.fixture
    def sample(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': 'Main attic',
            'typeEnglish': 'Attic/gable',
            'typeFrench': 'Combles/pignon',
            'nominalRsi': 2.864,
            'effectiveRsi': 2.9463,
            'area': 46.4515,
            'length': 23.875,
        }

    def test_from_data(self, sample: typing.Dict[str, typing.Any]):
        output = extracted_datatypes.Ceiling.from_data(sample)
        assert output.label == 'Main attic'
        assert output.area_metres == 46.4515

    def test_to_dict(self, sample: typing.Dict[str, typing.Any]) -> None:
        output = extracted_datatypes.Ceiling.from_data(sample).to_dict()
        assert output['areaMetres'] == sample['area']


class TestFloor:

    @pytest.fixture
    def sample(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': 'Rm over garage',
            'nominalRsi': 2.46,
            'effectiveRsi': 2.9181,
            'area': 9.2903,
            'length': 3.048,
        }

    def test_from_data(self, sample: typing.Dict[str, typing.Any]) -> None:
        output = extracted_datatypes.Floor.from_data(sample)
        assert output.label == 'Rm over garage'
        assert output.area_metres == 9.2903

    def test_to_dict(self, sample: typing.Dict[str, typing.Any]) -> None:
        output = extracted_datatypes.Floor.from_data(sample).to_dict()
        assert output['areaMetres'] == sample['area']
