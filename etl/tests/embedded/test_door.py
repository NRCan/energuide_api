import pytest
from energuide import bilingual
from energuide import element
from energuide.embedded import door
from energuide.embedded import distance
from energuide.embedded import insulation
from energuide.exceptions import InvalidEmbeddedDataTypeError


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


BAD_DATA_XML = [
    # This XML block has non-numeric strings for Measurements/@height and Measurements/@width
    """
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
    """,

    # This XML block is missing the <Type> tag
    """
    <Door>
        <Label>Front door</Label>
        <Construction>
        </Construction>
        <Measurements height='1.9799' width='0.8499' />
    </Door>
    """,

    #This XML block is missing the Measurements/@height and Measurements/@width attributes
    """
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
]


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


@pytest.mark.parametrize("bad_xml", BAD_DATA_XML)
def test_bad_data(bad_xml: str) -> None:
    door_node = element.Element.from_string(bad_xml)
    with pytest.raises(InvalidEmbeddedDataTypeError) as excinfo:
        door.Door.from_data(door_node)

    assert excinfo.value.data_class == door.Door


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
