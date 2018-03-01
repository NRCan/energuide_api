import typing
import pytest
from energuide import element
from energuide.embedded import area
from energuide.embedded import basement
from energuide.embedded import distance
from energuide.embedded import insulation
from energuide.exceptions import InvalidEmbeddedDataTypeError



@pytest.fixture
def sample_basement_floors_raw() -> str:
    return """
<Floor>
    <Construction isBelowFrostline="true" hasIntegralFooting="false" heatedFloor="false">
        <AddedToSlab rValue="0.1" nominalInsulation="0.2">User specified</AddedToSlab>
        <FloorsAbove idref="Code 8" rValue="0.6894" nominalInsulation="0.2">4231000660</FloorsAbove>
    </Construction>
    <Measurements isRectangular="true" length="2" width="2"/>
</Floor>
    """


@pytest.fixture
def sample_crawlspace_floors_raw() -> str:
    return """
<Floor>
    <Construction isBelowFrostline="false" hasIntegralFooting="false" heatedFloor="false">
        <FloorsAbove idref="Code 15" rValue="0.468" nominalInsulation="0">4200000000</FloorsAbove>
    </Construction>
    <Measurements isRectangular="true" width="4.9987" length="4.9999" />
</Floor>
    """


@pytest.fixture
def sample_basement_wall_raw() -> str:
    return """
<Wall hasPonyWall="true">
    <Construction corners="4">
        <InteriorAddedInsulation idref="Code 17" nominalInsulation="1.4">
            <Description>2101010</Description>s
            <Composite>
                <Section rank="1" percentage="50" rsi="1.2" nominalRsi="1.3" />
                <Section rank="2" rsi="1.5" nominalRsi="1.7" />
            </Composite>
        </InteriorAddedInsulation>
        <ExteriorAddedInsulation nominalInsulation="0">
            <Description>User specified</Description>
            <Composite>
                <Section rank="1" percentage="100" rsi="0" nominalRsi="0" />
            </Composite>
        </ExteriorAddedInsulation>
        <PonyWallType nominalInsulation="0">
          <Description>User specified</Description>
          <Composite>
              <Section rank="1" percentage="100" rsi="0" nominalRsi="0" />
          </Composite>
        </PonyWallType>
        <Lintels idref="Code 10">Bsmnt Lintel</Lintels>
    </Construction>
    <Measurements height="2.4384" depth="1.8288" ponyWallHeight="0.9144" />
</Wall>
    """


@pytest.fixture
def sample_crawlspace_wall_raw() -> str:
    return """
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
    """


@pytest.fixture
def sample_basement_header_raw() -> str:
    return """
<FloorHeader adjacentEnclosedSpace="false" id="3">
    <Label>BW hdr-01</Label>
    <Construction>
        <Type rValue="2.6892" nominalInsulation="3.3615">0000000000</Type>
    </Construction>
    <Measurements height="0.23" perimeter="34.7456" />
    <FacingDirection code="1">
        <English>N/A</English>
        <French>S/O</French>
    </FacingDirection>
</FloorHeader>
    """


@pytest.fixture
def sample_basement_raw(
        sample_basement_header_raw: str,
        sample_basement_wall_raw: str,
        sample_basement_floors_raw: str) -> str:

    return f"""
<Basement isExposedSurface="true" exposedSurfacePerimeter="34.7466" id="1">
    <Label>Foundation - 2</Label>
    <Configuration type="BBEN" subtype="1" overlap="0">BCIN_1</Configuration>
    {sample_basement_floors_raw}
    {sample_basement_wall_raw}
    <Components>
        {sample_basement_header_raw}
    </Components>
</Basement>
    """


@pytest.fixture
def sample_crawlspace_raw(
        sample_crawlspace_floors_raw: str,
        sample_crawlspace_wall_raw: str,
        sample_basement_header_raw: str) -> str:

    return f"""
<Crawlspace isExposedSurface="true" exposedSurfacePerimeter="9.144" id="29">
    <Label>Crawl</Label>
    <Configuration type="SCN" subtype="1">SCN_1</Configuration>
    {sample_crawlspace_floors_raw}
    {sample_crawlspace_wall_raw}
    <Components>
        {sample_basement_header_raw}
    </Components>
</Crawlspace>
    """


@pytest.fixture
def sample_basement_floors_element(sample_basement_floors_raw: str) -> element.Element:
    return element.Element.from_string(sample_basement_floors_raw)


@pytest.fixture
def sample_crawlspace_floors_element(sample_crawlspace_floors_raw: str) -> element.Element:
    return element.Element.from_string(sample_crawlspace_floors_raw)


@pytest.fixture
def sample_basement_wall_element(sample_basement_wall_raw: str) -> element.Element:
    return element.Element.from_string(sample_basement_wall_raw)


@pytest.fixture
def sample_crawlspace_wall_element(sample_crawlspace_wall_raw: str):
    return element.Element.from_string(sample_crawlspace_wall_raw)


@pytest.fixture
def sample_basement_header_element(sample_basement_header_raw: str) -> element.Element:
    return element.Element.from_string(sample_basement_header_raw)


@pytest.fixture
def sample_basement_element(sample_basement_raw: str) -> element.Element:
    return element.Element.from_string(sample_basement_raw)


@pytest.fixture
def sample_crawlspace_element(sample_crawlspace_raw: str) -> element.Element:
    return element.Element.from_string(sample_crawlspace_raw)


@pytest.fixture
def sample_slab_element() -> element.Element:
    xml = """
<Slab isExposedSurface="true" exposedSurfacePerimeter="6.096" id="30">
    <Label>Slab</Label>
    <Configuration type="SCN" subtype="1">SCN_1</Configuration>
    <Floor>
        <Construction isBelowFrostline="false" hasIntegralFooting="false" heatedFloor="false" />
        <Measurements isRectangular="true" width="3.048" length="6.096" />
    </Floor>
</Slab>
    """
    return element.Element.from_string(xml)

@pytest.fixture
def sample_basement_walls() -> typing.List[basement.BasementWall]:
    return [
        basement.BasementWall(
            wall_type=basement.WallType.INTERIOR,
            nominal_insulation=insulation.Insulation(rsi=1.3),
            effective_insulation=insulation.Insulation(rsi=1.2),
            composite_percentage=50.0,
            wall_area=area.Area(9.7536)),
        basement.BasementWall(
            wall_type=basement.WallType.INTERIOR,
            nominal_insulation=insulation.Insulation(rsi=1.7),
            effective_insulation=insulation.Insulation(rsi=1.5),
            composite_percentage=50.0,
            wall_area=area.Area(9.7536)),
        basement.BasementWall(
            wall_type=basement.WallType.EXTERIOR,
            nominal_insulation=insulation.Insulation(rsi=0.0),
            effective_insulation=insulation.Insulation(rsi=0.0),
            composite_percentage=100.0,
            wall_area=area.Area(19.5072)),
        basement.BasementWall(
            wall_type=basement.WallType.PONY,
            nominal_insulation=insulation.Insulation(rsi=0.0),
            effective_insulation=insulation.Insulation(rsi=0.0),
            composite_percentage=100.0,
            wall_area=area.Area(7.3152)),
    ]


@pytest.fixture
def sample_crawlspace_walls() -> typing.List[basement.BasementWall]:
    return [
        basement.BasementWall(
            wall_type=basement.WallType.NOT_APPLICABLE,
            nominal_insulation=insulation.Insulation(rsi=1.432),
            effective_insulation=insulation.Insulation(rsi=1.7968),
            composite_percentage=100.0,
            wall_area=area.Area(21.333012959999998)
        )
    ]


@pytest.fixture
def sample_basement_floors() -> typing.List[basement.BasementFloor]:
    return [basement.BasementFloor(
        floor_type=basement.FloorType.SLAB,
        rectangular=True,
        nominal_insulation=insulation.Insulation(rsi=0.2),
        effective_insulation=insulation.Insulation(rsi=0.1),
        length=distance.Distance(distance_metres=2.0),
        width=distance.Distance(distance_metres=2.0),
        perimeter=distance.Distance(distance_metres=8.0),
        floor_area=area.Area(4.0)
    )]


@pytest.fixture
def sample_crawlspace_floors() -> typing.List[basement.BasementFloor]:
    return [
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
    ]


@pytest.fixture
def sample_slab_floors() -> typing.List[basement.BasementFloor]:
    return [
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
    ]


@pytest.fixture
def sample_basement_header() -> basement.BasementHeader:
    return basement.BasementHeader(
        nominal_insulation=insulation.Insulation(rsi=3.3615),
        effective_insulation=insulation.Insulation(rsi=2.6892),
        height=distance.Distance(distance_metres=0.23),
        perimeter=distance.Distance(distance_metres=34.7456)
    )


@pytest.fixture
def sample_basement(
        sample_basement_floors: typing.List[basement.BasementFloor],
        sample_basement_walls: typing.List[basement.BasementWall],
        sample_basement_header: basement.BasementHeader,
    ) -> basement.Basement:

    return basement.Basement(
        foundation_type=basement.FoundationType.BASEMENT,
        label='Foundation - 2',
        configuration_type='BBEN',
        walls=sample_basement_walls,
        floors=sample_basement_floors,
        header=sample_basement_header
    )


@pytest.fixture
def sample_crawlspace(
        sample_crawlspace_floors: typing.List[basement.BasementFloor],
        sample_crawlspace_walls: typing.List[basement.BasementWall],
        sample_basement_header: basement.BasementHeader,
    ) -> basement.Basement:

    return basement.Basement(
        foundation_type=basement.FoundationType.CRAWLSPACE,
        label='Crawl',
        configuration_type='SCN',
        walls=sample_crawlspace_walls,
        floors=sample_crawlspace_floors,
        header=sample_basement_header,
    )


@pytest.fixture
def sample_slab(sample_slab_floors: typing.List[basement.BasementFloor]) -> basement.Basement:
    return basement.Basement(
        foundation_type=basement.FoundationType.SLAB,
        label='Slab',
        configuration_type='SCN',
        walls=[],
        floors=sample_slab_floors,
        header=None,
    )


def test_basement_walls_from_data(
        sample_basement_walls: typing.List[basement.BasementWall],
        sample_basement_wall_element: element.Element) -> None:

    output = basement.BasementWall.from_basement(sample_basement_wall_element, 8)
    assert output == sample_basement_walls


def test_crawlspace_walls_from_data(
        sample_crawlspace_walls: typing.List[basement.BasementWall],
        sample_crawlspace_wall_element: element.Element) -> None:

    output = basement.BasementWall.from_crawlspace(sample_crawlspace_wall_element, 19.9972)
    assert output == sample_crawlspace_walls


def test_basement_walls_to_dict(sample_basement_wall_element: element.Element) -> None:
    output = [wall.to_dict() for wall in basement.BasementWall.from_basement(sample_basement_wall_element, 8)]
    assert sorted(output, key=lambda wall: wall['percentage'])[0] == {
        'wallTypeEnglish': 'Interior',
        'wallTypeFrench': 'Intérieur',
        'insulationNominalRsi': 1.3,
        'insulationNominalR': 7.3817423381,
        'insulationEffectiveRsi': 1.2,
        'insulationEffectiveR': 6.813916004399999,
        'areaMetres': 9.7536,
        'areaFeet': 104.98688335958016,
        'percentage': 50.0,
    }


def test_crawlspace_walls_to_dict(sample_crawlspace_wall_element: element.Element) -> None:
    output = [wall.to_dict() for wall in basement.BasementWall.from_crawlspace(sample_crawlspace_wall_element, 19.9972)]
    assert sorted(output, key=lambda wall: wall['percentage'])[0] == {
        'wallTypeEnglish': 'Wall',
        'wallTypeFrench': 'Mur',
        'insulationNominalRsi': 1.432,
        'insulationNominalR': 8.131273098584,
        'insulationEffectiveRsi': 1.7968,
        'insulationEffectiveR': 10.202703563921599,
        'areaMetres': 21.333012959999998,
        'areaFeet': 229.62665511605272,
        'percentage': 100.0,
    }


def test_basement_floors_from_data(
        sample_basement_floors: typing.List[basement.BasementFloor],
        sample_basement_floors_element: element.Element) -> None:

    output = basement.BasementFloor.from_basement(sample_basement_floors_element)
    assert output == sample_basement_floors


def test_crawlspace_floors_from_data(
        sample_crawlspace_floors: typing.List[basement.BasementFloor],
        sample_crawlspace_floors_element: element.Element) -> None:

    output = basement.BasementFloor.from_crawlspace(sample_crawlspace_floors_element)
    assert output == sample_crawlspace_floors


def test_basement_floors_to_dict(sample_basement_floors_element: element.Element) -> None:
    output = [basement.to_dict()
              for basement in basement.BasementFloor.from_basement(sample_basement_floors_element)]
    assert output == [{
        'floorTypeEnglish': 'Slab',
        'floorTypeFrench': 'Dalle',
        'insulationNominalRsi': 0.2,
        'insulationNominalR': 1.1356526674,
        'insulationEffectiveRsi': 0.1,
        'insulationEffectiveR': 0.5678263337,
        'areaMetres': 4.0,
        'areaFeet': 43.0556444224,
        'perimeterMetres': 8.0,
        'perimeterFeet': 26.24672,
        'widthMetres': 2.0,
        'widthFeet': 6.56168,
        'lengthMetres': 2.0,
        'lengthFeet': 6.56168,
    }]


def test_crawlspace_floors_to_dict(sample_crawlspace_floors_element: element.Element) -> None:
    output = [basement.to_dict()
              for basement in basement.BasementFloor.from_crawlspace(sample_crawlspace_floors_element)]

    assert sorted(output, key=lambda basement: basement['floorTypeEnglish'])[0] == {
        'floorTypeEnglish': 'Floor above crawl space',
        'floorTypeFrench': 'Plancher au-dessus du vide sanitaire',
        'insulationNominalRsi': 0.0,
        'insulationNominalR': 0.0,
        'insulationEffectiveRsi': 0.468,
        'insulationEffectiveR': 2.657427241716,
        'areaMetres': 24.993000130000002,
        'areaFeet': 269.02243166156927,
        'perimeterMetres': 19.9972,
        'perimeterFeet': 65.607613648,
        'lengthMetres': 4.9999,
        'lengthFeet': 16.403871916,
        'widthMetres': 4.9987,
        'widthFeet': 16.399934908000002,
    }


def test_basement_header_from_data(
        sample_basement_header: basement.BasementHeader,
        sample_basement_header_element) -> None:

    output = basement.BasementHeader.from_data(sample_basement_header_element)
    assert output == sample_basement_header


def test_basement_header_to_dict(sample_basement_header_element: element.Element) -> None:
    output = basement.BasementHeader.from_data(sample_basement_header_element).to_dict()
    assert output == {
        'insulationNominalRsi': 3.3615,
        'insulationNominalR': 19.0874822073255,
        'insulationEffectiveRsi': 2.6892,
        'insulationEffectiveR': 15.2699857658604,
        'areaMetres': 7.991488000000001,
        'areaFeet': 86.01966643346914,
        'perimeterMetres': 34.7456,
        'perimeterFeet': 113.99475430400001,
        'heightMetres': 0.23,
        'heightFeet': 0.7545932000000001,
    }


def test_basement_from_data(
        sample_basement: basement.Basement,
        sample_basement_element: element.Element) -> None:
    output = basement.Basement.from_data(sample_basement_element)
    assert output == sample_basement


def test_crawlspace_from_data(
        sample_crawlspace: basement.Basement,
        sample_crawlspace_element: element.Element) -> None:
    output = basement.Basement.from_data(sample_crawlspace_element)
    assert output == sample_crawlspace


def test_slab_from_data(
        sample_slab: basement.Basement,
        sample_slab_element: element.Element) -> None:

    output = basement.Basement.from_data(sample_slab_element)
    assert output == sample_slab


def test_slab_to_dict(sample_slab_element: element.Element) -> None:
    output = basement.Basement.from_data(sample_slab_element).to_dict()
    assert output == {
        'foundationTypeEnglish': 'Slab',
        'foundationTypeFrench': 'Dalle',
        'label': 'Slab',
        'configurationType': 'SCN',
        'materialEnglish': 'concrete',
        'materialFrench': 'béton',
        'wall': [],
        'floors': [{
            'floorTypeEnglish': 'Slab',
            'floorTypeFrench': 'Dalle',
            'insulationNominalRsi': None,
            'insulationNominalR': None,
            'insulationEffectiveRsi': None,
            'insulationEffectiveR': None,
            'areaMetres': 18.580608,
            'areaFeet': 200.00001280000023,
            'perimeterMetres': 18.288,
            'perimeterFeet': 60.00000192,
            'lengthMetres': 6.096,
            'lengthFeet': 20.00000064,
            'widthMetres': 3.048,
            'widthFeet': 10.00000032,
        }],
        'header': None,
    }


def test_crawlspace_to_dict(sample_crawlspace_element: element.Element) -> None:
    output = basement.Basement.from_data(sample_crawlspace_element).to_dict()
    assert output == {
        'foundationTypeEnglish': 'Crawlspace',
        'foundationTypeFrench': 'Vide Sanitaire',
        'label': 'Crawl',
        'configurationType': 'SCN',
        'materialEnglish': 'concrete',
        'materialFrench': 'béton',
        'wall': [{
            'wallTypeEnglish': 'Wall',
            'wallTypeFrench': 'Mur',
            'insulationNominalRsi': 1.432,
            'insulationNominalR': 8.131273098584,
            'insulationEffectiveRsi': 1.7968,
            'insulationEffectiveR': 10.202703563921599,
            'areaMetres': 21.333012959999998,
            'areaFeet': 229.62665511605272,
            'percentage': 100.0,
        }],
        'floors': [{
            'floorTypeEnglish': 'Slab',
            'floorTypeFrench': 'Dalle',
            'insulationNominalRsi': None,
            'insulationNominalR': None,
            'insulationEffectiveRsi': None,
            'insulationEffectiveR': None,
            'areaMetres': 24.993000130000002,
            'areaFeet': 269.02243166156927,
            'perimeterMetres': 19.9972,
            'perimeterFeet': 65.607613648,
            'lengthMetres': 4.9999,
            'lengthFeet': 16.403871916,
            'widthMetres': 4.9987,
            'widthFeet': 16.399934908000002,
        }, {
            'floorTypeEnglish': 'Floor above crawl space',
            'floorTypeFrench': 'Plancher au-dessus du vide sanitaire',
            'insulationNominalRsi': 0.0,
            'insulationNominalR': 0.0,
            'insulationEffectiveRsi': 0.468,
            'insulationEffectiveR': 2.657427241716,
            'areaMetres': 24.993000130000002,
            'areaFeet': 269.02243166156927,
            'perimeterMetres': 19.9972,
            'perimeterFeet': 65.607613648,
            'lengthMetres': 4.9999,
            'lengthFeet': 16.403871916,
            'widthMetres': 4.9987,
            'widthFeet': 16.399934908000002,
        }],
        'header': {
            'insulationNominalRsi': 3.3615,
            'insulationNominalR': 19.0874822073255,
            'insulationEffectiveRsi': 2.6892,
            'insulationEffectiveR': 15.2699857658604,
            'areaMetres': 7.991488000000001,
            'areaFeet': 86.01966643346914,
            'perimeterMetres': 34.7456,
            'perimeterFeet': 113.99475430400001,
            'heightMetres': 0.23,
            'heightFeet': 0.7545932000000001,
        },
    }


def test_basement_to_dict(sample_basement_element: element.Element) -> None:
    output = basement.Basement.from_data(sample_basement_element).to_dict()
    assert output == {
        'foundationTypeEnglish': 'Basement',
        'foundationTypeFrench': 'Sous-sol',
        'label': 'Foundation - 2',
        'configurationType': 'BBEN',
        'materialEnglish': 'concrete and wood',
        'materialFrench': 'béton et bois',
        'wall': [{
            'wallTypeEnglish': 'Interior',
            'wallTypeFrench': 'Intérieur',
            'insulationNominalRsi': 1.3,
            'insulationNominalR': 7.3817423381,
            'insulationEffectiveRsi': 1.2,
            'insulationEffectiveR': 6.813916004399999,
            'areaMetres': 9.7536,
            'areaFeet': 104.98688335958016,
            'percentage': 50.0,
        }, {
            'wallTypeEnglish': 'Interior',
            'wallTypeFrench': 'Intérieur',
            'insulationNominalRsi': 1.7,
            'insulationNominalR': 9.6530476729,
            'insulationEffectiveRsi': 1.5,
            'insulationEffectiveR': 8.5173950055,
            'areaMetres': 9.7536,
            'areaFeet': 104.98688335958016,
            'percentage': 50.0,
        }, {
            'wallTypeEnglish': 'Exterior',
            'wallTypeFrench': 'Extérieur',
            'insulationNominalRsi': 0.0,
            'insulationNominalR': 0.0,
            'insulationEffectiveRsi': 0.0,
            'insulationEffectiveR': 0.0,
            'areaMetres': 19.5072,
            'areaFeet': 209.97376671916032,
            'percentage': 100.0,
        }, {
            'wallTypeEnglish': 'Pony Wall',
            'wallTypeFrench': 'Murs bas',
            'insulationNominalRsi': 0.0,
            'insulationNominalR': 0.0,
            'insulationEffectiveRsi': 0.0,
            'insulationEffectiveR': 0.0,
            'areaMetres': 7.3152,
            'areaFeet': 78.74016251968511,
            'percentage': 100.0,
        }],
        'floors': [{
            'floorTypeEnglish': 'Slab',
            'floorTypeFrench': 'Dalle',
            'insulationNominalRsi': 0.2,
            'insulationNominalR': 1.1356526674,
            'insulationEffectiveRsi': 0.1,
            'insulationEffectiveR': 0.5678263337,
            'areaMetres': 4.0,
            'areaFeet': 43.0556444224,
            'perimeterMetres': 8.0,
            'perimeterFeet': 26.24672,
            'widthMetres': 2.0,
            'widthFeet': 6.56168,
            'lengthMetres': 2.0,
            'lengthFeet': 6.56168,
        }],
        'header': {
            'insulationNominalRsi': 3.3615,
            'insulationNominalR': 19.0874822073255,
            'insulationEffectiveRsi': 2.6892,
            'insulationEffectiveR': 15.2699857658604,
            'areaMetres': 7.991488000000001,
            'areaFeet': 86.01966643346914,
            'perimeterMetres': 34.7456,
            'perimeterFeet': 113.99475430400001,
            'heightMetres': 0.23,
            'heightFeet': 0.7545932000000001,
        },
    }


def bad_xml() -> typing.List[typing.Tuple[str, typing.Callable[[element.Element], typing.Any], type]]:
    return [
        (
            # This XML block has non-numeric strings as attribute values
            """
            <Floor>
                <Construction isBelowFrostline="data" hasIntegralFooting="data" heatedFloor="data">
                    <AddedToSlab rValue="data" nominalInsulation="data">User specified</AddedToSlab>
                    <FloorsAbove idref="data" rValue="data" nominalInsulation="data">4231000660</FloorsAbove>
                </Construction>
                <Measurements isRectangular="data" length="data" width="data"/>
            </Floor>
            """,
            basement.BasementFloor.from_basement,
            basement.BasementFloor,
        ), (
            # This XML block has non-numeric strings as attribute values
            """
            <Floor>
                <Construction isBelowFrostline="data" hasIntegralFooting="data" heatedFloor="data">
                    <AddedToSlab rValue="data" nominalInsulation="data">User specified</AddedToSlab>
                    <FloorsAbove idref="data" rValue="data" nominalInsulation="data">4231000660</FloorsAbove>
                </Construction>
                <Measurements isRectangular="data" length="data" width="data"/>
            </Floor>
            """,
            basement.BasementFloor.from_crawlspace,
            basement.BasementFloor,
        ), (
            # This XML block is missing the attribute values of the Measurements tag
            """
            <Floor>
                <Construction isBelowFrostline="true" hasIntegralFooting="false" heatedFloor="false">
                    <AddedToSlab rValue="0.1" nominalInsulation="0.2">User specified</AddedToSlab>
                    <FloorsAbove idref="Code 8" rValue="0.6894" nominalInsulation="0.2">4231000660</FloorsAbove>
                </Construction>
                <Measurements />
            </Floor>
            """,
            basement.BasementFloor.from_basement,
            basement.BasementFloor,
        ), (
            # This XML block is missing the attribute values of the Measurements tag
            """
            <Floor>
                <Construction isBelowFrostline="true" hasIntegralFooting="false" heatedFloor="false">
                    <AddedToSlab rValue="0.1" nominalInsulation="0.2">User specified</AddedToSlab>
                    <FloorsAbove idref="Code 8" rValue="0.6894" nominalInsulation="0.2">4231000660</FloorsAbove>
                </Construction>
                <Measurements />
            </Floor>
            """,
            basement.BasementFloor.from_crawlspace,
            basement.BasementFloor,
        ), (
            # This XML block has non-numeric strings as attribute values
            """
            <Wall>
                <Construction corners="data">
                    <Type idref="data" nominalInsulation="data">
                        <Description>1211100700</Description>
                        <Composite>
                            <Section rank="data" percentage="data" rsi="data" nominalRsi="data" />
                        </Composite>
                    </Type>
                </Construction>
                <Measurements height="data" depth="data" />
                <RValues skirt="data" thermalBreak="data" />
            </Wall>
            """,
            lambda node: basement.BasementWall.from_crawlspace(node, 0),
            basement.BasementWall,
        ), (

            # This XML black is missing the percentage attribute of the Section tag
            """
            <Wall>
                <Construction corners="1">
                    <Type idref="Code 18" nominalInsulation="1.432">
                        <Description>1211100700</Description>
                        <Composite>
                            <Section rank="1" rsi="1.7968" nominalRsi="1.432" />
                        </Composite>
                    </Type>
                </Construction>
                <Measurements height="1.0668" depth="0.4572" />
                <RValues skirt="0" thermalBreak="0" />
            </Wall>
            """,
            lambda node: basement.BasementWall.from_crawlspace(node, 0),
            basement.BasementWall,
        ), (
            # This XML block is missing the height attribute of the Measurements tag
            """
            <Wall>
                <Construction corners="1">
                    <Type idref="Code 18" nominalInsulation="1.432">
                        <Description>1211100700</Description>
                        <Composite>
                            <Section rank="1" percentage="100" rsi="1.7968" nominalRsi="1.432" />
                        </Composite>
                    </Type>
                </Construction>
                <Measurements />
                <RValues skirt="0" thermalBreak="0" />
            </Wall>
            """,
            lambda node: basement.BasementWall.from_crawlspace(node, 0),
            basement.BasementWall,
        ), (
            # This XML block has non-numeric data as attribute values
            """
            <Wall hasPonyWall="data">
                <Construction corners="data">
                    <InteriorAddedInsulation idref="data" nominalInsulation="data">
                        <Description>2101010</Description>s
                        <Composite>
                            <Section rank="data" percentage="data" rsi="data" nominalRsi="data" />
                            <Section rank="data" percentage="data" rsi="data" nominalRsi="data" />
                        </Composite>
                    </InteriorAddedInsulation>
                    <Lintels idref="data">Bsmnt Lintel</Lintels>
                </Construction>
                <Measurements height="data" depth="data" ponyWallHeight="data" />
            </Wall>
            """,
            lambda node: basement.BasementWall.from_basement(node, 0),
            basement.BasementWall,
        ), (
            # This XML block is missing the height and ponyWallHeight attributes of the Measurments node
            """
            <Wall hasPonyWall="true">
                <Construction corners="4">
                    <InteriorAddedInsulation idref="Code 17" nominalInsulation="1.4">
                        <Description>2101010</Description>s
                        <Composite>
                            <Section rank="1" percentage="50" rsi="1.2" nominalRsi="1.3" />
                        </Composite>
                    </InteriorAddedInsulation>
                    <Lintels idref="Code 10">Bsmnt Lintel</Lintels>
                </Construction>
                <Measurements />
            </Wall>
            """,
            lambda node: basement.BasementWall.from_basement(node, 0),
            basement.BasementWall,
        ), (
            # This XML block is missing the percentage of it's Section tags
            """
            <Wall hasPonyWall="true">
                <Construction corners="4">
                    <InteriorAddedInsulation idref="Code 17" nominalInsulation="1.4">
                        <Description>2101010</Description>s
                        <Composite>
                            <Section rank="1" />
                        </Composite>
                    </InteriorAddedInsulation>
                </Construction>
                <Measurements height="2.4384" depth="1.8288" ponyWallHeight="0.9144" />
            </Wall>
            """,
            lambda node: basement.BasementWall.from_basement(node, 0),
            basement.BasementWall,
        ), (
            # This XML block has non-numeric strings as attribute values
            """
            <FloorHeader adjacentEnclosedSpace="data" id="data">
                <Label>BW hdr-01</Label>
                <Construction>
                    <Type rValue="data" nominalInsulation="data">0000000000</Type>
                </Construction>
                <Measurements height="data" perimeter="data" />
                <FacingDirection code="data">
                    <English>N/A</English>
                    <French>S/O</French>
                </FacingDirection>
            </FloorHeader>
            """,
            basement.BasementHeader.from_data,
            basement.BasementHeader,
        ), (
            # This XML block is missing the insulation attributes of the Type tag
            """
            <FloorHeader adjacentEnclosedSpace="false" id="3">
                <Label>BW hdr-01</Label>
                <Construction>
                    <Type >0000000000</Type>
                </Construction>
                <Measurements height="0.23" perimeter="34.7456" />
                <FacingDirection code="1">
                    <English>N/A</English>
                    <French>S/O</French>
                </FacingDirection>
            </FloorHeader>
            """,
            basement.BasementHeader.from_data,
            basement.BasementHeader,
        ), (
            # This XML block has an unknown foundation type tag
            """
            <SomeWeirdFoundation isExposedSurface="true" exposedSurfacePerimeter="34.7466" id="1">
                <Label>Foundation - 2</Label>
                <Configuration type="BBEN" subtype="1" overlap="0">BCIN_1</Configuration>
            </SomeWeirdFoundation>
            """,
            basement.Basement.from_data,
            basement.Basement,
        ), (
            # This XML block is missing the type attribute of teh Configuration tag
            """
            <Basement isExposedSurface="true" exposedSurfacePerimeter="34.7466" id="1">
                <Label>Foundation - 2</Label>
                <Configuration subtype="1" overlap="0">BCIN_1</Configuration>
            </Basement>
            """,
            basement.Basement.from_data,
            basement.Basement,
        ), (
            # This XML block is missing it's Label tag
            """
            <Crawlspace isExposedSurface="true" exposedSurfacePerimeter="9.144" id="29">
                <Configuration type="SCN" subtype="1">SCN_1</Configuration>
            </Crawlspace>
            """,
            basement.Basement.from_data,
            basement.Basement,
        ), (
            # This XML block has an empty string as the type attribute of the Configuration tag
            """
            <Crawlspace isExposedSurface="true" exposedSurfacePerimeter="9.144" id="29">
                <Label>Crawl</Label>
                <Configuration type="" subtype="1">SCN_1</Configuration>
            </Crawlspace>
            """,
            basement.Basement.from_data,
            basement.Basement,
        )
    ]

@pytest.mark.parametrize("bad_xml, parse_function, data_class", bad_xml())
def test_bad_data(bad_xml, parse_function, data_class) -> None:
    node = element.Element.from_string(bad_xml)
    with pytest.raises(InvalidEmbeddedDataTypeError) as excinfo:
        parse_function(node)

    assert excinfo.value.data_class is data_class
