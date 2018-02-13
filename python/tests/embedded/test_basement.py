import typing
import pytest
from energuide import element
from energuide.embedded import area
from energuide.embedded import basement
from energuide.embedded import distance
from energuide.embedded import insulation

@pytest.fixture
def sample_basement_floor_raw() -> str:
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
def sample_basement_wall_raw() -> str:
    return """
<Wall hasPonyWall="true">
    <Construction corners="4">
        <InteriorAddedInsulation idref="Code 17" nominalInsulation="1.4">
            <Description>2101010</Description>s
            <Composite>
                <Section rank="1" percentage="50" rsi="1.2" nominalRsi="1.3" />
                <Section rank="2" percentage="50" rsi="1.5" nominalRsi="1.7" />
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
        sample_basement_floor_raw: str) -> str:

    return f"""
<Basement isExposedSurface="true" exposedSurfacePerimeter="34.7466" id="1">
    <Label>Foundation - 2</Label>
    <Configuration type="BBEN" subtype="1" overlap="0">BCIN_1</Configuration>
    {sample_basement_floor_raw}
    {sample_basement_wall_raw}
    <Components>
        {sample_basement_header_raw}
    </Components>
</Basement>
    """


@pytest.fixture
def sample_basement_floor_element(sample_basement_floor_raw: str) -> element.Element:
    return element.Element.from_string(sample_basement_floor_raw)


@pytest.fixture
def sample_basement_wall_element(sample_basement_wall_raw: str) -> element.Element:
    return element.Element.from_string(sample_basement_wall_raw)


@pytest.fixture
def sample_basement_header_element(sample_basement_header_raw: str) -> element.Element:
    return element.Element.from_string(sample_basement_header_raw)


@pytest.fixture
def sample_basement_element(sample_basement_raw: str) -> element.Element:
    return element.Element.from_string(sample_basement_raw)


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
def sample_basement_floor() -> basement.BasementFloor:
    return basement.BasementFloor(
        rectangular=True,
        nominal_insulation=insulation.Insulation(rsi=0.2),
        effective_insulation=insulation.Insulation(rsi=0.1),
        length=distance.Distance(distance_metres=2.0),
        width=distance.Distance(distance_metres=2.0),
        perimeter=None,
        optional_area=None
    )


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
        sample_basement_floor,
        sample_basement_walls,
        sample_basement_header,
    ) -> basement.Basement:

    return basement.Basement(
        label='Foundation - 2',
        configuration_type='BBEN',
        walls=sample_basement_walls,
        floor=sample_basement_floor,
        header=sample_basement_header
    )

def test_basement_walls_from_data(
        sample_basement_walls: typing.List[basement.BasementWall],
        sample_basement_wall_element: element.Element) -> None:

    output = basement.BasementWall.from_data(sample_basement_wall_element, 8)
    assert output == sample_basement_walls


def test_basement_walls_to_dict(sample_basement_wall_element: element.Element) -> None:
    output = [wall.to_dict() for wall in basement.BasementWall.from_data(sample_basement_wall_element, 8)]
    assert sorted(output, key=lambda wall: wall['percentage'])[0] == {
        'wallTypeEnglish': 'Interior',
        'wallTypeFrench': 'Intérieur',
        'nominalRsi': 1.3,
        'nominalR': 7.3817423381,
        'effectiveRsi': 1.2,
        'effectiveR': 6.813916004399999,
        'areaMetres': 9.7536,
        'areaFeet': 104.98688335958016,
        'percentage': 50.0,
    }


def test_basement_floor_from_data(
        sample_basement_floor: basement.BasementFloor,
        sample_basement_floor_element: element.Element) -> None:

    output = basement.BasementFloor.from_data(sample_basement_floor_element)
    assert output == sample_basement_floor


def test_basement_floor_to_dict(sample_basement_floor_element: element.Element) -> None:
    output = basement.BasementFloor.from_data(sample_basement_floor_element).to_dict()
    assert output == {
        'nominalRsi': 0.2,
        'nominalR': 1.1356526674,
        'effectiveRsi': 0.1,
        'effectiveR': 0.5678263337,
        'areaMetres': 4.0,
        'areaFeet': 43.0556444224,
        'perimeterMetres': None,
        'perimeterFeet': None,
        'widthMetres': 2.0,
        'widthFeet': 6.56168,
        'lengthMetres': 2.0,
        'lengthFeet': 6.56168,
    }


def test_basement_header_from_data(
        sample_basement_header: basement.BasementHeader,
        sample_basement_header_element) -> None:

    output = basement.BasementHeader.from_data(sample_basement_header_element)
    assert output == sample_basement_header


def test_basement_header_to_dict(sample_basement_header_element: element.Element) -> None:
    output = basement.BasementHeader.from_data(sample_basement_header_element).to_dict()
    assert output == {
        'nominalRsi': 3.3615,
        'nominalR': 19.0874822073255,
        'effectiveRsi': 2.6892,
        'effectiveR': 15.2699857658604,
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


def test_basement_to_dict(sample_basement_element: element.Element) -> None:
    output = basement.Basement.from_data(sample_basement_element).to_dict()
    assert output == {
        'label': 'Foundation - 2',
        'configurationType': 'BBEN',
        'materialEnglish': 'concrete and wood',
        'materialFrench': 'béton et bois',
        'wall': [{
            'wallTypeEnglish': 'Interior',
            'wallTypeFrench': 'Intérieur',
            'nominalRsi': 1.3,
            'nominalR': 7.3817423381,
            'effectiveRsi': 1.2,
            'effectiveR': 6.813916004399999,
            'areaMetres': 9.7536,
            'areaFeet': 104.98688335958016,
            'percentage': 50.0,
        }, {
            'wallTypeEnglish': 'Interior',
            'wallTypeFrench': 'Intérieur',
            'nominalRsi': 1.7,
            'nominalR': 9.6530476729,
            'effectiveRsi': 1.5,
            'effectiveR': 8.5173950055,
            'areaMetres': 9.7536,
            'areaFeet': 104.98688335958016,
            'percentage': 50.0,
        }, {
            'wallTypeEnglish': 'Exterior',
            'wallTypeFrench': 'Extérieur',
            'nominalRsi': 0.0,
            'nominalR': 0.0,
            'effectiveRsi': 0.0,
            'effectiveR': 0.0,
            'areaMetres': 19.5072,
            'areaFeet': 209.97376671916032,
            'percentage': 100.0,
        }, {
            'wallTypeEnglish': 'Pony Wall',
            'wallTypeFrench': 'Murs bas',
            'nominalRsi': 0.0,
            'nominalR': 0.0,
            'effectiveRsi': 0.0,
            'effectiveR': 0.0,
            'areaMetres': 7.3152,
            'areaFeet': 78.74016251968511,
            'percentage': 100.0,
        }],
        'floor': {
            'nominalRsi': 0.2,
            'nominalR': 1.1356526674,
            'effectiveRsi': 0.1,
            'effectiveR': 0.5678263337,
            'areaMetres': 4.0,
            'areaFeet': 43.0556444224,
            'perimeterMetres': None,
            'perimeterFeet': None,
            'widthMetres': 2.0,
            'widthFeet': 6.56168,
            'lengthMetres': 2.0,
            'lengthFeet': 6.56168,
        },
        'header': {
            'nominalRsi': 3.3615,
            'nominalR': 19.0874822073255,
            'effectiveRsi': 2.6892,
            'effectiveR': 15.2699857658604,
            'areaMetres': 7.991488000000001,
            'areaFeet': 86.01966643346914,
            'perimeterMetres': 34.7456,
            'perimeterFeet': 113.99475430400001,
            'heightMetres': 0.23,
            'heightFeet': 0.7545932000000001,
        },
    }
