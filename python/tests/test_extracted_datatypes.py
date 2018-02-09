import typing
import pytest
from energuide import element
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
        ],
        'window': [
            {
                'id': 'Code 11',
                'label': '202002',
                'glazingTypesEnglish': 'Double/double with 1 coat',
                'glazingTypesFrench': 'Double/double, 1 couche',
                'coatingsTintsEnglish': 'Clear',
                'coatingsTintsFrench': 'Transparent',
                'fillTypeEnglish': '6 mm Air',
                'fillTypeFrench': "6 mm d'air",
                'spacerTypeEnglish': 'Metal',
                'spacerTypeFrench': 'Métal',
                'typeEnglish': 'Picture',
                'typeFrench': 'Fixe',
                'frameMaterialEnglish': 'Wood',
                'frameMaterialFrench': 'Bois',
            }, {
                'id': 'Code 12',
                'label': '234002',
                'glazingTypesEnglish': 'Double/double with 1 coat',
                'glazingTypesFrench': 'Double/double, 1 couche',
                'coatingsTintsEnglish': 'Low-E .20 (hard1)',
                'coatingsTintsFrench': 'Faible E .20 (Dur 1)',
                'fillTypeEnglish': '9 mm Argon',
                'fillTypeFrench': "9 mm d'argon",
                'spacerTypeEnglish': 'Metal',
                'spacerTypeFrench': 'Métal',
                'typeEnglish': 'Picture',
                'typeFrench': 'Fixe',
                'frameMaterialEnglish': 'Wood',
                'frameMaterialFrench': 'Bois',
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


class TestWindowCode:

    @pytest.fixture
    def sample(self, raw_codes: typing.Dict[str, typing.List[typing.Dict[str, str]]]) -> typing.Dict[str, str]:
        return raw_codes['window'][0]

    def test_from_data(self, sample: typing.Dict[str, str]) -> None:
        output = extracted_datatypes.WindowCode.from_data(sample)
        assert output.identifier == 'Code 11'
        assert output.label == '202002'


class TestCodes:

    def test_from_data(self, raw_codes: typing.Dict[str, typing.List[typing.Dict[str, str]]]) -> None:
        output = extracted_datatypes.Codes.from_data(raw_codes)
        assert len(output.wall) == 2
        assert len(output.window) == 2
        assert output.wall['Code 1'].structure_type_english == 'Wood frame'
        assert output.window['Code 11'].glazing_types_english == 'Double/double with 1 coat'


class TestHeatedFloorArea:

    @pytest.fixture
    def sample(self) -> typing.Dict[str, float]:
        return {
            'belowGrade': 185.8,
            'aboveGrade': 92.9,
        }

    def test_from_data(self, sample: typing.Dict[str, float]) -> None:
        output = extracted_datatypes.HeatedFloorArea.from_data(sample)
        assert output.area_above_grade == 92.9
        assert output.area_below_grade_feet == 1999.93468342048

    def test_to_dict(self, sample: typing.Dict[str, float]) -> None:
        output = extracted_datatypes.HeatedFloorArea.from_data(sample).to_dict()
        assert output['areaAboveGradeMetres'] == 92.9
        assert output['areaBelowGradeMetres'] == 185.8


class TestWindow:

    @pytest.fixture
    def sample(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': 'East0001',
            'constructionTypeCode': 'Code 12',
            'constructionTypeValue': '234002',
            'rsi': 0.4779,
            'width': 1967.738,
            'height': 1322.0699,
        }

    def test_from_data(self, sample: typing.Dict[str, typing.Any], codes: extracted_datatypes.Codes) -> None:
        output = extracted_datatypes.Window.from_data(sample, codes.window)
        assert output.label == 'East0001'
        assert output.width == 1.967738
        assert output.glazing_types_english == 'Double/double with 1 coat'

    def test_missing_optional_fields(self,
                                     sample: typing.Dict[str, typing.Any],
                                     codes: extracted_datatypes.Codes) -> None:
        window = sample.copy()
        window.pop('constructionTypeCode')
        window.pop('constructionTypeValue')
        output = extracted_datatypes.Window.from_data(window, codes.window)
        assert output.label == 'East0001'
        assert output.width == 1.967738
        assert output.glazing_types_english is None

    def test_to_dict(self,
                     sample: typing.Dict[str, typing.Any],
                     codes: extracted_datatypes.Codes) -> None:
        output = extracted_datatypes.Window.from_data(sample, codes.window).to_dict()
        assert output['areaMetres'] == (sample['width'] * 0.001) * (sample['height'] * 0.001)


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

    def test_from_data(self, sample: typing.Dict[str, typing.Any], codes: extracted_datatypes.Codes) -> None:
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
    def sample(self) -> element.Element:
        data = """
<Ceiling>
    <Label>Main attic</Label>
    <Construction>
        <Type>
            <English>Attic/gable</English>
            <French>Combles/pignon</French>
        </Type>
        <CeilingType nominalInsulation='2.864' rValue='2.9463' />
    </Construction>
    <Measurements area='46.4515' length='23.875' />
</Ceiling>
        """
        return element.Element.from_string(data)

    def test_from_data(self, sample: element.Element):
        output = extracted_datatypes.Ceiling.from_data(sample)
        assert output.label == 'Main attic'
        assert output.area_metres == 46.4515

    def test_to_dict(self, sample: element.Element) -> None:
        output = extracted_datatypes.Ceiling.from_data(sample).to_dict()
        assert output['areaMetres'] == 46.4515

    def test_properties(self, sample: element.Element) -> None:
        output = extracted_datatypes.Ceiling.from_data(sample)
        assert output.nominal_r == 16.262546197168
        assert output.effective_r == 16.729867269803098
        assert output.area_feet == 499.9998167217784
        assert output.length_feet == 78.330055


class TestFloor:

    @pytest.fixture
    def sample(self) -> element.Element:
        doc = """
        <Floor>
            <Label>Rm over garage</Label>
            <Construction>
                <Type nominalInsulation='2.46' rValue='2.9181' />
            </Construction>
            <Measurements area='9.2903' length='3.048' />
        </Floor>
        """
        return element.Element.from_string(doc)

    def test_from_data(self, sample: element.Element) -> None:
        output = extracted_datatypes.Floor.from_data(sample)
        assert output.label == 'Rm over garage'
        assert output.area_metres == 9.2903

    def test_to_dict(self, sample: element.Element) -> None:
        output = extracted_datatypes.Floor.from_data(sample).to_dict()
        assert output['areaMetres'] == 9.2903

    def test_properties(self, sample: element.Element) -> None:
        output = extracted_datatypes.Floor.from_data(sample)
        assert output.nominal_r == 13.96852780902
        assert output.effective_r == 16.569740243699698
        assert output.area_feet == 99.99996334435568
        assert output.length_feet == 10.00000032


class TestDoor:

    @pytest.fixture
    def sample(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': 'Front door',
            'typeEnglish': 'Solid wood',
            'typeFrench': 'Bois massif',
            'rsi': 0.39,
            'height': 1.9799,
            'width': 0.8499,
        }

    def test_from_data(self, sample: typing.Dict[str, typing.Any]) -> None:
        output = extracted_datatypes.Door.from_data(sample)
        assert output.type_english == 'Solid wood'
        assert output.rsi == 0.39

    def test_to_dict(self, sample: typing.Dict[str, typing.Any]) -> None:
        output = extracted_datatypes.Door.from_data(sample).to_dict()
        assert output == {
            'typeEnglish': 'Solid wood',
            'typeFrench': 'Bois massif',
            'rsi': 0.39,
            'rValue': 2.21452270143,
            'uFactor': 2.564102564102564,
            'uFactorImperial': 0.45156457387149956,
            'areaMetres': 1.68271701,
            'areaFeet': 18.112616311521026,
        }
