import pytest
from energuide import bilingual
from energuide import element
from energuide import extracted_datatypes
from energuide.embedded import code

# pylint: disable=no-self-use


@pytest.fixture
def codes() -> code.Codes:
    wall_code = code.WallCode(
        identifier='Code 1',
        label='1201101121',
        structure_type=bilingual.Bilingual(
            english='Wood frame',
            french='Ossature de bois',
        ),
        component_type_size=bilingual.Bilingual(
            english='38x89 mm (2x4 in)',
            french='38x89 (2x4)',
        )
    )

    window_code = code.WindowCode(
        identifier='Code 11',
        label='202002',
        glazing_type=bilingual.Bilingual(
            english='Double/double with 1 coat',
            french='Double/double, 1 couche',
        ),
        coating_tint=bilingual.Bilingual(english='Clear', french='Transparent'),
        fill_type=bilingual.Bilingual(english='6 mm Air', french="6 mm d'air"),
        spacer_type=bilingual.Bilingual(english='Metal', french='Métal'),
        window_code_type=bilingual.Bilingual(english='Picture', french='Fixe'),
        frame_material=bilingual.Bilingual(english='Wood', french='Bois'),
    )

    return code.Codes(
        wall={wall_code.identifier: wall_code},
        window={window_code.identifier: window_code}
    )


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
                <Type idref='Code 11' rValue='0.4779'>234002</Type>
            </Construction>
            <Measurements width='1967.738' height='1322.0699' />
        </Window>
        """
        return element.Element.from_string(doc)

    def test_from_data(self, sample: element.Element, codes: code.Codes) -> None:
        output = extracted_datatypes.Window.from_data(sample, codes.window)
        assert output.label == 'East0001'
        assert output.width == 1.967738
        assert output.glazing_type_english == 'Double/double with 1 coat'

    def test_missing_optional_fields(self, codes: code.Codes) -> None:
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
        assert output.glazing_type_english is None

    def test_to_dict(self,
                     sample: element.Element,
                     codes: code.Codes) -> None:
        output = extracted_datatypes.Window.from_data(sample, codes.window).to_dict()
        assert output['areaMetres'] == 2.6014871808862


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


class TestWaterHeating:

    @pytest.fixture
    def sample(self) -> element.Element:
        data = """
<HotWater>
    <Primary hasDrainWaterHeatRecovery="false" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
        <EquipmentInformation>
            <Manufacturer>Wizard DHW man</Manufacturer>
            <Model>Wizard DHW mod</Model>
        </EquipmentInformation>
        <EnergySource code="1">
            <English>Electricity</English>
            <French>Électricité</French>
        </EnergySource>
        <TankType code="2">
            <English>Conventional tank</English>
            <French>Réservoir classique</French>
        </TankType>
        <TankVolume code="4" value="189.3001">
            <English>189.3 L, 41.6 Imp, 50 US gal</English>
            <French>189.3 L, 41.6 imp, 50 gal ÉU</French>
        </TankVolume>
        <EnergyFactor code="1" value="0.8217" inputCapacity="0">
            <English>Use defaults</English>
            <French>Valeurs par défaut</French>
        </EnergyFactor>
        <TankLocation code="2">
            <English>Basement</English>
            <French>Sous-sol</French>
        </TankLocation>
    </Primary>
</HotWater>
        """
        return element.Element.from_string(data)

    def test_from_data(self, sample: element.Element) -> None:
        output = extracted_datatypes.WaterHeating.from_data(sample)[0]
        assert output.type_english == extracted_datatypes.WaterHeaterType.ELECTRICITY_CONVENTIONAL_TANK_ENGLISH
        assert output.efficiency == 0.8217

    def test_to_dict(self, sample: element.Element) -> None:
        output = extracted_datatypes.WaterHeating.from_data(sample)[0].to_dict()
        assert output == {
            'typeEnglish': 'Electric storage tank',
            'typeFrench': 'Réservoir électrique',
            'tankVolumeLitres': 189.3001,
            'TankVolumeGallon': 50.0077860172,
            'efficiency': 0.8217,
        }

    def test_properties(self, sample: element.Element) -> None:
        output = extracted_datatypes.WaterHeating.from_data(sample)[0]
        assert output.tank_volume_gallon == 50.0077860172
