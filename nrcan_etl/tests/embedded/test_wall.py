import typing
import pytest
from energuide import bilingual
from energuide import element
from energuide.embedded import code
from energuide.embedded import distance
from energuide.embedded import insulation
from energuide.embedded import wall
from energuide.exceptions import InvalidEmbeddedDataTypeError


@pytest.fixture
def raw_sample() -> element.Element:
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

BAD_XML_DATA = [
    # This XML block is missing the <Label> tag
    """
    <Wall>
        <Construction>
            <Type nominalInsulation='1.432' rValue='1.8016'><User specified/Type>
        </Construction>
        <Measurements perimeter='42.9768' height='2.4384' />
    </Wall>
    """,

    # This XML block has non-numeric strings as attribute values
    """
    <Wall>
        <Label>Second level</Label>
        <Construction>
            <Type nominalInsulation='bad' rValue='data'><User specified/Type>
        </Construction>
        <Measurements perimeter='is' height='here' />
    </Wall>
    """,

    #This XML block is missing the attributes for the <Type> tag
    """
    <Wall>
        <Label>Second level</Label>
        <Construction>
            <Type><User specified/Type>
        </Construction>
        <Measurements />
    </Wall>
    """
]

@pytest.fixture
def sample_wall_code() -> typing.Dict[str, code.WallCode]:
    return {'Code 1': code.WallCode(
        identifier='Code 1',
        label='1201101121',
        tags={
            code.WallCodeTag.STRUCTURE_TYPE: bilingual.Bilingual(
                english='Wood frame',
                french='Ossature de bois',
            ),
            code.WallCodeTag.COMPONENT_TYPE_SIZE: bilingual.Bilingual(
                english='38x89 mm (2x4 in)',
                french='38x89 (2x4)',
            )
        },
    )}


@pytest.fixture
def sample(sample_wall_code: typing.Dict[str, code.WallCode]) -> wall.Wall:
    return wall.Wall(
        label='Second level',
        wall_code=sample_wall_code['Code 1'],
        nominal_insulation=insulation.Insulation(1.432),
        effective_insulation=insulation.Insulation(1.8016),
        perimeter=distance.Distance(42.9768),
        height=distance.Distance(2.4384),
    )


def test_from_data(raw_sample: element.Element,
                   sample_wall_code: typing.Dict[str, code.WallCode],
                   sample: wall.Wall) -> None:
    output = wall.Wall.from_data(raw_sample, sample_wall_code)
    assert output == sample


def test_from_data_missing_codes() -> None:
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
    output = wall.Wall.from_data(sample, {})
    assert output.label == 'Test Floor'
    assert output.wall_code is None
    assert output.to_dict()['structureTypeEnglish'] is None


@pytest.mark.parametrize("bad_xml", BAD_XML_DATA)
def test_bad_data(bad_xml: str) -> None:
    wall_node = element.Element.from_string(bad_xml)
    with pytest.raises(InvalidEmbeddedDataTypeError) as excinfo:
        wall.Wall.from_data(wall_node, {})

    assert excinfo.value.data_class == wall.Wall


def test_to_dict(sample: wall.Wall) -> None:
    output = sample.to_dict()
    assert output == {
        'label': 'Second level',
        'structureTypeEnglish': 'Wood frame',
        'structureTypeFrench': 'Ossature de bois',
        'componentTypeSizeEnglish': '38x89 mm (2x4 in)',
        'componentTypeSizeFrench': '38x89 (2x4)',
        'insulationNominalRsi': 1.432,
        'insulationNominalR': 8.131273098584,
        'insulationEffectiveRsi': 1.8016,
        'insulationEffectiveR': 10.2299592279392,
        'areaMetres': 104.79462912,
        'areaFeet': 1128.0000721920012,
        'perimeterMetres': 42.9768,
        'perimeterFeet': 141.000004512,
        'heightMetres': 2.4384,
        'heightFeet': 8.000000256,
    }
