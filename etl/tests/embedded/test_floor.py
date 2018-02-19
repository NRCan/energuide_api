import pytest
from energuide import element
from energuide.embedded import area
from energuide.embedded import distance
from energuide.embedded import floor
from energuide.embedded import insulation
from energuide.exceptions import InvalidEmbeddedDataTypeError


@pytest.fixture
def sample_raw() -> element.Element:
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

BAD_XML_DATA = [
    # This XML block is missing the <Label> tag
    """
    <Floor>
        <Construction>
            <Type nominalInsulation='2.46' rValue='2.9181' />
        </Construction>
        <Measurements area='9.2903' length='3.048' />
    </Floor>
    """,

    # This XML has non-numeric strings as attribute values
    """
    <Floor>
        <Label>Rm over garage</Label>
        <Construction>
            <Type nominalInsulation='bad' rValue='data' />
        </Construction>
        <Measurements area='goes' length='here' />
    </Floor>
    """,

    # This XML block is missing all attributes for <Type> and <Measurements> tags
    """
    <Floor>
        <Label>Rm over garage</Label>
        <Construction>
            <Type />
        </Construction>
        <Measurements />
    </Floor>
    """,
]


@pytest.fixture
def sample() -> floor.Floor:
    return floor.Floor(
        label='Rm over garage',
        nominal_insulation=insulation.Insulation(2.46),
        effective_insulation=insulation.Insulation(2.9181),
        floor_area=area.Area(9.2903),
        floor_length=distance.Distance(3.048),
    )


def test_from_data(sample_raw: element.Element, sample: floor.Floor) -> None:
    output = floor.Floor.from_data(sample_raw)
    assert output == sample


@pytest.mark.parametrize("bad_xml", BAD_XML_DATA)
def test_bad_data(bad_xml: str) -> None:
    floor_node = element.Element.from_string(bad_xml)
    with pytest.raises(InvalidEmbeddedDataTypeError) as excinfo:
        floor.Floor.from_data(floor_node)

    assert excinfo.value.data_class == floor.Floor


def test_to_dict(sample: floor.Floor) -> None:
    output = sample.to_dict()
    assert output == {
        'label': 'Rm over garage',
        'insulationNominalRsi': 2.46,
        'insulationNominalR': 13.96852780902,
        'insulationEffectiveRsi': 2.9181,
        'insulationEffectiveR': 16.569740243699698,
        'areaMetres': 9.2903,
        'areaFeet': 99.99996334435568,
        'lengthMetres': 3.048,
        'lengthFeet': 10.00000032,
    }
