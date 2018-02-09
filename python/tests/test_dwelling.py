import copy
import datetime
import typing
import pytest
from energuide import dwelling
from energuide import reader
from energuide import extracted_datatypes


# pylint: disable=no-self-use

@pytest.fixture
def ceiling_input() -> typing.List[str]:
    doc = """
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
    return [doc]


@pytest.fixture
def floor_input() -> typing.List[str]:
    doc = """
    <Floor>
        <Label>Rm over garage</Label>
        <Construction>
            <Type nominalInsulation='2.46' rValue='2.9181' />
        </Construction>
        <Measurements area='9.2903' length='3.048' />
    </Floor>
    """
    return [doc]


@pytest.fixture
def wall_input() -> typing.List[str]:
    doc = """
    <Wall>
            <Label>Second level</Label>
            <Construction>
                <Type idref='Code 1' nominalInsulation='1.432' rValue='1.8016' />
            </Construction>
            <Measurements perimeter='42.9768' height='2.4384' />
        </Wall>
    """
    return [doc]


@pytest.fixture
def door_input() -> typing.List[str]:
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
    return [doc]


@pytest.fixture
def window_input() -> typing.List[str]:
    doc = """
    <Window>
        <Label>East0001</Label>
        <Construction>
            <Type idref='Code 12' rValue='0.4779'>234002</Type>
        </Construction>
        <Measurements width='1967.738' height='1322.0699' />
    </Window>
    """
    return [doc]


@pytest.fixture
def heated_floor_area_input() -> str:
    return """
    <HeatedFloorArea aboveGrade="92.9" belowGrade="185.8" />
    """


@pytest.fixture
def heating_cooling_input() -> str:
    return """
    <HeatingCooling id="25">
            <Label>Heating/Cooling System</Label>
            <CoolingSeason>
                <Start code="1">January</Start>
                <End code="12">December</End>
                <Design code="7">July</Design>
            </CoolingSeason>
            <Type1>
                <FansAndPump hasEnergyEfficientMotor="false">
                    <Mode code="1">
                        <English>Auto</English>
                        <French>Auto</French>
                    </Mode>
                    <Power isCalculated="true" low="0" high="640.2" />
                </FansAndPump>
                <Furnace>
                    <EquipmentInformation energystar="false">
                        <Manufacturer>Wizard SPH man</Manufacturer>
                    </EquipmentInformation>
                    <Equipment isBiEnergy="false" switchoverTemperature="0">
                        <EnergySource code="2">
                            <English>Natural gas</English>
                            <French>Gaz naturel</French>
                        </EnergySource>
                        <EquipmentType code="1">
                            <English>Furnace w/ continuous pilot</English>
                            <French>Fournaise avec veilleuse permanente</French>
                        </EquipmentType>
                    </Equipment>
                    <Specifications sizingFactor="1.1" efficiency="78" isSteadyState="true" pilotLight="25.3" flueDiameter="152.4">
                        <OutputCapacity code="2" value="33" uiUnits="btu/hr">
                            <English>Calculated</English>
                            <French>Calculé</French>
                        </OutputCapacity>
                    </Specifications>
                </Furnace>
            </Type1>
            <Type2 shadingInF280Cooling="AccountedFor" />
            <MultipleSystems>
                <Summary energySaverHeatingSystems="0" energySaverAirSourceHeatPump="0" woodAppliances="0" epaCsaHeatingSystems="0" />
            </MultipleSystems>
            <SupplementaryHeatingSystems>
                <System rank="1">
                    <EquipmentInformation csaEpa="false" />
                    <Equipment>
                        <EnergySource code="5">
                            <English>Mixed Wood</English>
                            <French>Bois mélangé</French>
                        </EnergySource>
                        <Type code="1">
                            <English>Advanced airtight wood stove</English>
                            <French>Poêle à bois étanche avancé</French>
                        </Type>
                    </Equipment>
                    <Specifications efficiency="30" damperClosed="false">
                        <YearMade code="7">
                            <English>1970-79</English>
                            <French>1970-79</French>
                        </YearMade>
                        <Usage code="1">
                            <English>Never</English>
                            <French>Jamais</French>
                        </Usage>
                        <LocationHeated code="1" value="12.0031">
                            <English>Main Floors</English>
                            <French>Plancher Principaux</French>
                        </LocationHeated>
                        <Flue isInterior="true" diameter="127">
                            <Type code="1">
                                <English>Brick</English>
                                <French>Brique</French>
                            </Type>
                        </Flue>
                        <OutputCapacity value="2" uiUnits="kW" />
                    </Specifications>
                </System>
            </SupplementaryHeatingSystems>
        </HeatingCooling>
    """


@pytest.fixture
def ventilation_input() -> typing.List[str]:
    doc = """
<Hrv supplyFlowrate="220" exhaustFlowrate="220" fanPower1="509.14" isDefaultFanpower="true" isEnergyStar="false" isHomeVentilatingInstituteCertified="false" isSupplemental="false" temperatureCondition1="0" temperatureCondition2="-25" fanPower2="624.08" efficiency1="55" efficiency2="45" preheaterCapacity="0" lowTempVentReduction="0" coolingEfficiency="25">
    <EquipmentInformation />
    <VentilatorType code="1">
        <English>HRV</English>
        <French>VRC</French>
    </VentilatorType>
    <ColdAirDucts>
        <Supply length="1.5" diameter="152.4" insulation="0.7">
            <Location code="4">
                <English>Main floor</English>
                <French>Rez-de-chaussée</French>
            </Location>
            <Type code="1">
                <English>Flexible</English>
                <French>Flexible</French>
            </Type>
            <Sealing code="2">
                <English>Sealed</English>
                <French>Scellé</French>
            </Sealing>
        </Supply>
        <Exhaust length="1.5" diameter="152.4" insulation="0.7">
            <Location code="4">
                <English>Main floor</English>
                <French>Rez-de-chaussée</French>
            </Location>
            <Type code="1">
                <English>Flexible</English>
                <French>Flexible</French>
            </Type>
            <Sealing code="2">
                <English>Sealed</English>
                <French>Scellé</French>
            </Sealing>
        </Exhaust>
    </ColdAirDucts>
</Hrv>
    """
    return [doc]


@pytest.fixture
def water_heating_input() -> typing.List[str]:
    doc = """
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
    return doc


@pytest.fixture
def raw_codes() -> typing.Dict[str, typing.List[str]]:
    return {
        'wall': [
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
        ],
        'window': [
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
    }


@pytest.fixture
def sample_input_d(ceiling_input: typing.List[str],
                   floor_input: typing.List[str],
                   wall_input: typing.List[str],
                   door_input: typing.List[str],
                   window_input: typing.List[str],
                   heated_floor_area_input: str,
                   heating_cooling_input: str,
                   ventilation_input: typing.List[str],
                   water_heating_input: str,
                   raw_codes: typing.Dict[str, typing.List[str]]) -> reader.InputData:

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
        'ceilings': ceiling_input,
        'floors': floor_input,
        'walls': wall_input,
        'doors': door_input,
        'windows': window_input,
        'heating_cooling': heating_cooling_input,
        'heatedFloorArea': heated_floor_area_input,
        'ventilations': ventilation_input,
        'waterHeatings': water_heating_input,
        'codes': raw_codes,
    }


@pytest.fixture
def sample_input_e(sample_input_d: reader.InputData) -> reader.InputData:
    output = copy.deepcopy(sample_input_d)
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
            ],
            walls=[
                extracted_datatypes.Wall(
                    label='Second level',
                    structure_type_english='Wood frame',
                    structure_type_french='Ossature de bois',
                    component_type_size_english='38x89 mm (2x4 in)',
                    component_type_size_french='38x89 (2x4)',
                    nominal_rsi=1.432,
                    effective_rsi=1.8016,
                    perimeter=42.9768,
                    height=2.4384,
                )
            ],
            doors=[
                extracted_datatypes.Door(
                    label='Front door',
                    type_english='Solid wood',
                    type_french='Bois massif',
                    rsi=0.39,
                    height=1.9799,
                    width=0.8499,
                )
            ],
            windows=[
                extracted_datatypes.Window(
                    label='East0001',
                    glazing_types_english='Double/double with 1 coat',
                    glazing_types_french='Double/double, 1 couche',
                    coatings_tints_english='Low-E .20 (hard1)',
                    coatings_tints_french='Faible E .20 (Dur 1)',
                    fill_type_english='9 mm Argon',
                    fill_type_french="9 mm d'argon",
                    spacer_type_english='Metal',
                    spacer_type_french='Métal',
                    type_english='Picture',
                    type_french='Fixe',
                    frame_material_english='Wood',
                    frame_material_french='Bois',
                    rsi=0.4779,
                    width=1.967738,
                    height=1.3220699,
                )
            ],
            heated_floor_area=extracted_datatypes.HeatedFloorArea(
                area_above_grade=92.9,
                area_below_grade=185.8,
            ),
            ventilations=[
                extracted_datatypes.Ventilation(
                    type_english='Heat recovery ventilator',
                    type_french='Ventilateur-récupérateur de chaleur',
                    air_flow_rate=220,
                    efficiency=55,
                )
            ],
            water_heatings=[
                extracted_datatypes.WaterHeating(
                    type_english='Electric storage tank',
                    type_french='Réservoir électrique',
                    tank_volume=189.3001,
                    efficiency=0.8217,
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
        return [sample_input_d, sample_input_e].copy()

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
