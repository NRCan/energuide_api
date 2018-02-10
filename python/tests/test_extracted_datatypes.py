import typing
import pytest
from energuide import element
from energuide import extracted_datatypes

# pylint: disable=no-self-use


@pytest.fixture
def raw_wall_codes() -> typing.List[element.Element]:
    data = [
        """
        <Code id='Code 1'>
            <Label>1201101121</Label>
            <Layers>
                <StructureType>
                    <English>Wood frame</English>
                    <French>Ossature de bois</French>
                </StructureType>
                <ComponentTypeSize>
                    <English>38x89 mm (2x4 in)</English>
                    <French>38x89 (2x4)</French>
                </ComponentTypeSize>
            </Layers>
        </Code>
        """,
        """
        <Code id='Code 2'>
            <Label>1201101121</Label>
            <Layers>
                <StructureType>
                    <English>Metal frame</English>
                    <French>Ossature de métal</French>
                </StructureType>
                <ComponentTypeSize>
                    <English>38x89 mm (2x4 in)</English>
                    <French>38x89 (2x4)</French>
                </ComponentTypeSize>
            </Layers>
        </Code>
        """,
    ]
    return [element.Element.from_string(code) for code in data]


@pytest.fixture
def raw_window_codes() -> typing.List[element.Element]:
    data = [
        """
        <Code id='Code 11'>
            <Label>202002</Label>
            <Layers>
                <GlazingTypes>
                    <English>Double/double with 1 coat</English>
                    <French>Double/double, 1 couche</French>
                </GlazingTypes>
                <CoatingsTints>
                    <English>Clear</English>
                    <French>Transparent</French>
                </CoatingsTints>
                <FillType>
                    <English>6 mm Air</English>
                    <French>6 mm d'air</French>
                </FillType>
                <SpacerType>
                    <English>Metal</English>
                    <French>Métal</French>
                </SpacerType>
                <Type>
                    <English>Picture</English>
                    <French>Fixe</French>
                </Type>
                <FrameMaterial>
                    <English>Wood</English>
                    <French>Bois</French>
                </FrameMaterial>
            </Layers>
        </Code>
        """,
        """
        <Code id='Code 12'>
            <Label>234002</Label>
            <Layers>
                <GlazingTypes>
                    <English>Double/double with 1 coat</English>
                    <French>Double/double, 1 couche</French>
                </GlazingTypes>
                <CoatingsTints>
                    <English>Low-E .20 (hard1)</English>
                    <French>Faible E .20 (Dur 1)</French>
                </CoatingsTints>
                <FillType>
                    <English>9 mm Argon</English>
                    <French>9 mm d'argon</French>
                </FillType>
                <SpacerType>
                    <English>Metal</English>
                    <French>Métal</French>
                </SpacerType>
                <Type>
                    <English>Picture</English>
                    <French>Fixe</French>
                </Type>
                <FrameMaterial>
                    <English>Wood</English>
                    <French>Bois</French>
                </FrameMaterial>
            </Layers>
        </Code>
        """,
    ]
    return [element.Element.from_string(code) for code in data]


@pytest.fixture
def raw_codes(raw_wall_codes: typing.List[element.Element],
              raw_window_codes: typing.List[element.Element]) -> typing.Dict[str, typing.List[element.Element]]:
    return {
        'wall': raw_wall_codes,
        'window': raw_window_codes,
    }


@pytest.fixture
def codes(raw_codes: typing.Dict[str, typing.List[element.Element]]) -> extracted_datatypes.Codes:
    return extracted_datatypes.Codes.from_data(raw_codes)


class TestWallCode:

    def test_from_data(self, raw_wall_codes: typing.List[element.Element]) -> None:
        output = [extracted_datatypes.WallCode.from_data(raw_code) for raw_code in raw_wall_codes]
        assert output[0].identifier == 'Code 1'
        assert output[0].label == '1201101121'


class TestWindowCode:

    def test_from_data(self, raw_window_codes: typing.List[element.Element]) -> None:
        output = [extracted_datatypes.WindowCode.from_data(raw_code) for raw_code in raw_window_codes]
        assert output[0].identifier == 'Code 11'
        assert output[0].label == '202002'


class TestCodes:

    def test_from_data(self, raw_codes: typing.Dict[str, typing.List[element.Element]]) -> None:
        output = extracted_datatypes.Codes.from_data(raw_codes)
        assert len(output.wall) == 2
        assert len(output.window) == 2
        assert output.wall['Code 1'].structure_type_english == 'Wood frame'
        assert output.window['Code 11'].glazing_types_english == 'Double/double with 1 coat'


class TestHeatedFloorArea:

    @pytest.fixture
    def sample(self) -> element.Element:
        doc = """
        <HeatedFloorArea aboveGrade="92.9" belowGrade="185.8" />
        """
        return element.Element.from_string(doc)

    def test_from_data(self, sample: element.Element) -> None:
        output = extracted_datatypes.HeatedFloorArea.from_data(sample)
        assert output.area_above_grade == 92.9
        assert output.area_below_grade_feet == 1999.93468342048

    def test_to_dict(self, sample: element.Element) -> None:
        output = extracted_datatypes.HeatedFloorArea.from_data(sample).to_dict()
        assert output['areaAboveGradeMetres'] == 92.9
        assert output['areaBelowGradeMetres'] == 185.8

    def test_properties(self, sample: element.Element) -> None:
        output = extracted_datatypes.HeatedFloorArea.from_data(sample)
        assert output.area_above_grade_feet == 999.96734171024
        assert output.area_below_grade_feet == 1999.93468342048


class TestWindow:

    @pytest.fixture
    def sample(self) -> element.Element:
        doc = """
        <Window>
            <Label>East0001</Label>
            <Construction>
                <Type idref='Code 12' rValue='0.4779'>234002</Type>
            </Construction>
            <Measurements width='1967.738' height='1322.0699' />
        </Window>
        """
        return element.Element.from_string(doc)

    def test_from_data(self, sample: element.Element, codes: extracted_datatypes.Codes) -> None:
        output = extracted_datatypes.Window.from_data(sample, codes.window)
        assert output.label == 'East0001'
        assert output.width == 1.967738
        assert output.glazing_types_english == 'Double/double with 1 coat'

    def test_missing_optional_fields(self, codes: extracted_datatypes.Codes) -> None:
        doc = """
        <Window>
            <Label>East0001</Label>
            <Construction>
                <Type rValue='0.4779' />
            </Construction>
            <Measurements width='1967.738' height='1322.0699' />
        </Window>
        """
        window = element.Element.from_string(doc)
        output = extracted_datatypes.Window.from_data(window, codes.window)
        assert output.label == 'East0001'
        assert output.width == 1.967738
        assert output.glazing_types_english is None

    def test_to_dict(self,
                     sample: element.Element,
                     codes: extracted_datatypes.Codes) -> None:
        output = extracted_datatypes.Window.from_data(sample, codes.window).to_dict()
        assert output['areaMetres'] == 2.6014871808862


class TestWall:

    @pytest.fixture
    def sample(self) -> element.Element:
        doc = """
        <Wall>
            <Label>Second level</Label>
            <Construction>
                <Type idref='Code 1' nominalInsulation='1.432' rValue='1.8016' />
            </Construction>
            <Measurements perimeter='42.9768' height='2.4384' />
        </Wall>
        """
        return element.Element.from_string(doc)

    def test_from_data(self, sample: element.Element, codes: extracted_datatypes.Codes) -> None:
        output = extracted_datatypes.Wall.from_data(sample, codes.wall)
        assert output.label == 'Second level'
        assert output.perimeter == 42.9768

    def test_from_data_missing_codes(self, codes: extracted_datatypes.Codes) -> None:
        doc = """
        <Wall>
            <Label>Test Floor</Label>
            <Construction>
                <Type rValue="2.6892" nominalInsulation="3.3615">User specified</Type>
            </Construction>
            <Measurements perimeter='42.9768' height='2.4384' />
        </Wall>
        """
        sample = element.Element.from_string(doc)
        output = extracted_datatypes.Wall.from_data(sample, codes.wall)
        assert output.label == 'Test Floor'
        assert output.structure_type_english is None

    def test_to_dict(self, sample: element.Element, codes: extracted_datatypes.Codes) -> None:
        output = extracted_datatypes.Wall.from_data(sample, codes.wall).to_dict()
        assert output['areaMetres'] == 42.9768 * 2.4384

    def test_properties(self, sample: element.Element, codes: extracted_datatypes.Codes) -> None:
        output = extracted_datatypes.Wall.from_data(sample, codes.wall)
        assert output.nominal_r == 8.131273098584
        assert output.effective_r == 10.2299592279392
        assert output.area_metres == 104.79462912
        assert output.area_feet == 1128.0000721920012


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
    def sample(self) -> element.Element:
        doc = """
        <Door>
            <Label>Front door</Label>
            <Construction>
                <Type value='0.39'>
                    <English>Solid wood</English>
                    <French>Bois massif</French>
                </Type>
            </Construction>
            <Measurements height='1.9799' width='0.8499' />
        </Door>
        """
        return element.Element.from_string(doc)

    def test_from_data(self, sample: element.Element) -> None:
        output = extracted_datatypes.Door.from_data(sample)
        assert output.type_english == 'Solid wood'
        assert output.rsi == 0.39

    def test_to_dict(self, sample: element.Element) -> None:
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

    def test_properties(self, sample: element.Element) -> None:
        output = extracted_datatypes.Door.from_data(sample)
        assert output.r_value == 2.21452270143
        assert output.u_factor == 2.564102564102564
        assert output.u_factor_imperial == 0.45156457387149956
        assert output.area_metres == 1.68271701
        assert output.area_feet == 18.112616311521027


class TestVentilation:

    @pytest.fixture
    def sample(self) -> element.Element:
        data = """
<Hrv supplyFlowrate="220" exhaustFlowrate="220" fanPower1="509.14" isDefaultFanpower="true" isEnergyStar="false" isHomeVentilatingInstituteCertified="false" isSupplemental="false" temperatureCondition1="0" temperatureCondition2="-25" fanPower2="624.08" efficiency1="55" efficiency2="45" preheaterCapacity="0" lowTempVentReduction="0" coolingEfficiency="25">
    <EquipmentInformation />
    <VentilatorType code="1">
        <English>HRV</English>
        <French>VRC</French>
    </VentilatorType>
</Hrv>
        """
        return element.Element.from_string(data)

    def test_from_data(self, sample: element.Element):
        output = extracted_datatypes.Ventilation.from_data(sample)
        assert output.ventilation_type == extracted_datatypes.VentilationType.NOT_ENERGY_STAR_NOT_INSTITUTE_CERTIFIED
        assert output.air_flow_rate == 220

    def test_to_dict(self, sample: element.Element) -> None:
        output = extracted_datatypes.Ventilation.from_data(sample).to_dict()
        assert output == {
            'typeEnglish': 'Heat recovery ventilator',
            'typeFrench': 'Ventilateur-récupérateur de chaleur',
            'airFlowRateLps': 220,
            'airFlowRateCfm': 466.1536,
            'efficiency': 55,
        }

    def test_properties(self, sample: element.Element) -> None:
        output = extracted_datatypes.Ventilation.from_data(sample)
        assert output.air_flow_rate_cmf == 466.1536
