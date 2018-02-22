import copy
import datetime
import typing
import pytest
from energuide import bilingual
from energuide import dwelling
from energuide import reader
from energuide.embedded import area
from energuide.embedded import ceiling
from energuide.embedded import code
from energuide.embedded import distance
from energuide.embedded import floor
from energuide.embedded import heating
from energuide.embedded import insulation
from energuide.embedded import wall
from energuide.embedded import door
from energuide.embedded import window
from energuide.embedded import water_heating
from energuide.embedded import ventilation
from energuide.embedded import heated_floor_area
from energuide.embedded import basement
from energuide.exceptions import InvalidInputDataError
from energuide.exceptions import InvalidGroupSizeError


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
def water_heating_input() -> str:
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
def basement_input() -> typing.List[str]:
    doc = """
    <Basement isExposedSurface="true" exposedSurfacePerimeter="35.052" id="1">
        <Label>Basement</Label>
        <Configuration type="BCCB" subtype="4" overlap="0">BCCB_4</Configuration>
        <Floor>
            <Construction isBelowFrostline="true" hasIntegralFooting="false" heatedFloor="false">
                <AddedToSlab rValue="0" nominalInsulation="0">User specified</AddedToSlab>
                <FloorsAbove idref="Code 16" rValue="0.7059" nominalInsulation="0">4231000660</FloorsAbove>
            </Construction>
            <Measurements isRectangular="false" area="92.903" perimeter="39.9297" />
        </Floor>
        <Wall hasPonyWall="false">
            <Construction corners="4">
                <InteriorAddedInsulation idref="Code 17" nominalInsulation="1.432">
                    <Description>2101010</Description>
                    <Composite>
                        <Section rank="1" percentage="100" rsi="1.4603" nominalRsi="1.432" />
                    </Composite>
                </InteriorAddedInsulation>
                <Lintels idref="Code 10">Bsmnt Lintel</Lintels>
            </Construction>
            <Measurements height="2.4384" depth="1.8288" ponyWallHeight="0" />
        </Wall>
        <Components>
            <FloorHeader adjacentEnclosedSpace="false" id="6">
                <Label>BW hdr-01</Label>
                <Construction>
                    <Type idref="Code 21" rValue="4.0777" nominalInsulation="3.87">1800400220</Type>
                </Construction>
                <Measurements height="0.23" perimeter="39.9288" />
                <FacingDirection code="1">
                    <English>N/A</English>
                    <French>S/O</French>
                </FacingDirection>
            </FloorHeader>
        </Components>
    </Basement>
    """
    return [doc]


@pytest.fixture
def crawlspace_input() -> typing.List[str]:
    doc = """
    <Crawlspace isExposedSurface="true" exposedSurfacePerimeter="9.144" id="29">
        <Label>Crawl</Label>
        <Configuration type="SCN" subtype="1">SCN_1</Configuration>
        <Floor>
            <Construction isBelowFrostline="false" hasIntegralFooting="false" heatedFloor="false">
                <FloorsAbove idref="Code 15" rValue="0.468" nominalInsulation="0">4200000000</FloorsAbove>
            </Construction>
            <Measurements isRectangular="true" width="4.9987" length="4.9999" />
        </Floor>
        <Wall>
            <Construction corners="1">
                <Type idref="Code 18" nominalInsulation="1.432">
                    <Description>1211100700</Description>
                    <Composite>
                        <Section rank="1" percentage="100" rsi="1.7968" nominalRsi="1.432" />
                    </Composite>
                </Type>
            </Construction>
            <Measurements height="1.0668" depth="0.4572" />
            <RValues skirt="0" thermalBreak="0" />
        </Wall>
        <Components>
            <FloorHeader adjacentEnclosedSpace="false" id="6">
                <Label>BW hdr-01</Label>
                <Construction>
                    <Type idref="Code 21" rValue="4.0777" nominalInsulation="3.87">1800400220</Type>
                </Construction>
                <Measurements height="0.23" perimeter="39.9288" />
                <FacingDirection code="1">
                    <English>N/A</English>
                    <French>S/O</French>
                </FacingDirection>
            </FloorHeader>
        </Components>
    </Crawlspace>
    """
    return [doc]


@pytest.fixture
def slab_input() -> typing.List[str]:
    doc = """
    <Slab isExposedSurface="true" exposedSurfacePerimeter="6.096" id="30">
        <Label>Slab</Label>
        <Configuration type="SCN" subtype="1">SCN_1</Configuration>
        <Floor>
            <Construction isBelowFrostline="false" hasIntegralFooting="false" heatedFloor="false" />
            <Measurements isRectangular="true" width="3.048" length="6.096" />
        </Floor>
        <Wall>
            <RValues skirt="0" thermalBreak="0" />
        </Wall>
    </Slab>
    """
    return [doc]


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
                   basement_input: typing.List[str],
                   crawlspace_input: typing.List[str],
                   slab_input: typing.List[str],
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
        'basements': basement_input,
        'crawlspaces': crawlspace_input,
        'slabs': slab_input,
        'codes': raw_codes,
        'ERSRATING': '567'
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
            identifier='Code 12',
            label='234002',
            glazing_type=bilingual.Bilingual(
                english='Double/double with 1 coat',
                french='Double/double, 1 couche',
            ),
            coating_tint=bilingual.Bilingual(english='Low-E .20 (hard1)', french='Faible E .20 (Dur 1)'),
            fill_type=bilingual.Bilingual(english='9 mm Argon', french="9 mm d'argon"),
            spacer_type=bilingual.Bilingual(english='Metal', french='Métal'),
            window_code_type=bilingual.Bilingual(english='Picture', french='Fixe'),
            frame_material=bilingual.Bilingual(english='Wood', french='Bois'),
        )

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
            ers_rating=567,
            ceilings=[
                ceiling.Ceiling(
                    label='Main attic',
                    ceiling_type=bilingual.Bilingual(english='Attic/gable', french='Combles/pignon'),
                    nominal_insulation=insulation.Insulation(2.864),
                    effective_insulation=insulation.Insulation(2.9463),
                    ceiling_area=area.Area(46.4515),
                    ceiling_length=distance.Distance(23.875),
                )
            ],
            floors=[
                floor.Floor(
                    label='Rm over garage',
                    nominal_insulation=insulation.Insulation(2.46),
                    effective_insulation=insulation.Insulation(2.9181),
                    floor_area=area.Area(9.2903),
                    floor_length=distance.Distance(3.048),
                )
            ],
            walls=[
                wall.Wall(
                    label='Second level',
                    wall_code=wall_code,
                    nominal_insulation=insulation.Insulation(1.432),
                    effective_insulation=insulation.Insulation(1.8016),
                    perimeter=distance.Distance(42.9768),
                    height=distance.Distance(2.4384),
                )
            ],
            doors=[
                door.Door(
                    label='Front door',
                    door_type=bilingual.Bilingual(english='Solid wood', french='Bois massif'),
                    door_insulation=insulation.Insulation(0.39),
                    height=distance.Distance(1.9799),
                    width=distance.Distance(0.8499),
                )
            ],
            windows=[
                window.Window(
                    label='East0001',
                    window_code=window_code,
                    window_insulation=insulation.Insulation(0.4779),
                    width=distance.Distance(1.967738),
                    height=distance.Distance(1.3220699),
                )
            ],
            heated_floor=heated_floor_area.HeatedFloorArea(
                area_above_grade=area.Area(92.9),
                area_below_grade=area.Area(185.8),
            ),
            ventilations=[
                ventilation.Ventilation(
                    ventilation_type=ventilation.VentilationType.NOT_ENERGY_STAR_NOT_INSTITUTE_CERTIFIED,
                    air_flow_rate=220.0,
                    efficiency=55.0,
                )
            ],
            water_heatings=[
                water_heating.WaterHeating(
                    water_heater_type=water_heating.WaterHeaterType.ELECTRICITY_CONVENTIONAL_TANK,
                    tank_volume=189.3001,
                    efficiency=0.8217,
                )
            ],
            heating_system=heating.Heating(
                heating_type=heating.HeatingType.FURNACE,
                energy_source=heating.EnergySource.NATURAL_GAS,
                equipment_type=bilingual.Bilingual(english='Furnace w/ continuous pilot',
                                                   french='Fournaise avec veilleuse permanente'),
                label='Heating/Cooling System',
                output_size=0.009671344275824395,
                efficiency=78.0,
                steady_state='Steady State',
            ),
            foundations=[
                basement.Basement(
                    foundation_type=basement.FoundationType.BASEMENT,
                    label='Basement',
                    configuration_type='BCCB',
                    walls=[
                        basement.BasementWall(
                            wall_type=basement.WallType.INTERIOR,
                            nominal_insulation=insulation.Insulation(rsi=1.432),
                            effective_insulation=insulation.Insulation(rsi=1.4603),
                            composite_percentage=100.0,
                            wall_area=area.Area(97.36458048)
                        )
                    ],
                    floors=[
                        basement.BasementFloor(
                            floor_type=basement.FloorType.SLAB,
                            rectangular=False,
                            nominal_insulation=insulation.Insulation(rsi=0.0),
                            effective_insulation=insulation.Insulation(rsi=0.0),
                            length=None,
                            width=None,
                            perimeter=distance.Distance(distance_metres=39.9297),
                            floor_area=area.Area(92.903)
                        )
                    ],
                    header=basement.BasementHeader(
                        nominal_insulation=insulation.Insulation(rsi=3.87),
                        effective_insulation=insulation.Insulation(rsi=4.0777),
                        height=distance.Distance(distance_metres=0.23),
                        perimeter=distance.Distance(distance_metres=39.9288)
                    ),
                ),
                basement.Basement(
                    foundation_type=basement.FoundationType.CRAWLSPACE,
                    label='Crawl',
                    configuration_type='SCN',
                    walls=[
                        basement.BasementWall(
                            wall_type=basement.WallType.NOT_APPLICABLE,
                            nominal_insulation=insulation.Insulation(rsi=1.432),
                            effective_insulation=insulation.Insulation(rsi=1.7968),
                            composite_percentage=100.0,
                            wall_area=area.Area(21.333012959999998)
                        )
                    ],
                    floors=[
                        basement.BasementFloor(
                            floor_type=basement.FloorType.SLAB,
                            rectangular=True,
                            nominal_insulation=None,
                            effective_insulation=None,
                            width=distance.Distance(distance_metres=4.9987),
                            length=distance.Distance(distance_metres=4.9999),
                            perimeter=distance.Distance(distance_metres=19.9972),
                            floor_area=area.Area(24.993000130000002)
                        ), basement.BasementFloor(
                            floor_type=basement.FloorType.FLOOR_ABOVE_CRAWLSPACE,
                            rectangular=True,
                            nominal_insulation=insulation.Insulation(rsi=0.0),
                            effective_insulation=insulation.Insulation(rsi=0.468),
                            width=distance.Distance(distance_metres=4.9987),
                            length=distance.Distance(distance_metres=4.9999),
                            perimeter=distance.Distance(distance_metres=19.9972),
                            floor_area=area.Area(24.993000130000002)
                        )
                    ],
                    header=basement.BasementHeader(
                        nominal_insulation=insulation.Insulation(rsi=3.87),
                        effective_insulation=insulation.Insulation(rsi=4.0777),
                        height=distance.Distance(distance_metres=0.23),
                        perimeter=distance.Distance(distance_metres=39.9288)
                    ),
                ),
                basement.Basement(
                    foundation_type=basement.FoundationType.SLAB,
                    label='Slab',
                    configuration_type='SCN',
                    walls=[],
                    floors=[
                        basement.BasementFloor(
                            floor_type=basement.FloorType.SLAB,
                            rectangular=True,
                            nominal_insulation=None,
                            effective_insulation=None,
                            width=distance.Distance(distance_metres=3.048),
                            length=distance.Distance(distance_metres=6.096),
                            perimeter=distance.Distance(distance_metres=18.288),
                            floor_area=area.Area(18.580608)
                        )
                    ],
                    header=None,
                ),
            ],
        )

    def test_bad_postal_code(self, sample_input_d: reader.InputData) -> None:
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

    def test_missing_ers(self, sample_input_d: reader.InputData) -> None:
        sample_input_d['ERSRATING'] = ''
        output = dwelling.ParsedDwellingDataRow.from_row(sample_input_d)
        assert output.ers_rating is None


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
        with pytest.raises(InvalidGroupSizeError):
            dwelling.Dwelling.from_group(data)

    def test_to_dict(self, sample: typing.List[reader.InputData]) -> None:
        output = dwelling.Dwelling.from_group(sample).to_dict()
        assert output['houseId'] == 123
        assert len(output['evaluations']) == 2
        assert 'postalCode' not in output
        assert output['region'] == dwelling.Region.ONTARIO.value
