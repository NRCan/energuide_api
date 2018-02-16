import pytest
from energuide import bilingual
from energuide import element
from energuide.embedded import door
from energuide.embedded import distance
from energuide.embedded import insulation
from energuide.exceptions import InvalidEmbeddedDataTypeException


@pytest.fixture
def sample_raw() -> element.Element:
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


@pytest.fixture
def bad_measurements() -> element.Element:
    doc = """
    <Door>
        <Label>Front door</Label>
        <Construction>
            <Type value='0.39'>
                <English>Solid wood</English>
                <French>Bois massif</French>
            </Type>
        </Construction>
        <Measurements height='bad' width='data' />
    </Door>
    """
    return element.Element.from_string(doc)


@pytest.fixture
def missing_type() -> element.Element:
    doc = """
    <Door>
        <Label>Front door</Label>
        <Construction>
        </Construction>
        <Measurements height='1.9799' width='0.8499' />
    </Door>
    """
    return element.Element.from_string(doc)


@pytest.fixture
def bad_insulation() -> element.Element:
    doc = """
    <Door>
        <Label>Front door</Label>
        <Construction>
            <Type value='0.39'>
                <English>Solid wood</English>
                <French>Bois massif</French>
            </Type>
        </Construction>
        <Measurements />
    </Door>
    """
    return element.Element.from_string(doc)


@pytest.fixture
def sample() -> door.Door:
    return door.Door(
        label='Front door',
        door_type=bilingual.Bilingual(english='Solid wood', french='Bois massif'),
        door_insulation=insulation.Insulation(0.39),
        height=distance.Distance(1.9799),
        width=distance.Distance(0.8499),
    )


def test_from_data(sample_raw: element.Element, sample: door.Door) -> None:
    output = door.Door.from_data(sample_raw)
    assert output == sample


def test_bad_measurements(bad_measurements: element.Element) -> None:
    with pytest.raises(InvalidEmbeddedDataTypeException) as excinfo:
        door.Door.from_data(bad_measurements)

    assert isinstance(excinfo.value.__context__, ValueError)


def test_missing_type(missing_type: element.Element) -> None:
    with pytest.raises(InvalidEmbeddedDataTypeException) as excinfo:
        door.Door.from_data(missing_type)

    assert isinstance(excinfo.value.__context__, AssertionError)


def test_bad_insulation(bad_insulation: element.Element) -> None:
    with pytest.raises(InvalidEmbeddedDataTypeException) as excinfo:
        door.Door.from_data(bad_insulation)

    assert isinstance(excinfo.value.__context__, IndexError)


def test_to_dict(sample: door.Door) -> None:
    output = sample.to_dict()
    assert output == {
        'typeEnglish': 'Solid wood',
        'typeFrench': 'Bois massif',
        'insulationRsi': 0.39,
        'insulationR': 2.21452270143,
        'uFactor': 2.564102564102564,
        'uFactorImperial': 0.45156457387149956,
        'areaMetres': 1.68271701,
        'areaFeet': 18.112616311521026,
    }


def test_properties(sample_raw: element.Element) -> None:
    output = door.Door.from_data(sample_raw)
    assert output.u_factor == 2.564102564102564
    assert output.u_factor_imperial == 0.45156457387149956
