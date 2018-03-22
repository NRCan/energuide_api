import typing
import pytest
from energuide import bilingual
from energuide import element
from energuide.embedded import code
from energuide.embedded import distance
from energuide.embedded import insulation
from energuide.embedded import window
from energuide.exceptions import InvalidEmbeddedDataTypeError


@pytest.fixture
def raw_sample() -> element.Element:
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


BAD_XML_DATA = [
    # This XML block is missing the <Label> tag
    """
    <Window>
        <Construction>
            <Type rValue='0.4779'>User specified</Type>
        </Construction>
        <Measurements width='1967.738' height='1322.0699' />
    </Window>
    """,

    # This XML block has non-numeric strings as attribute values
    """
    <Window>
        <Label>East0001</Label>
        <Construction>
            <Type rValue='bad'>User specified</Type>
        </Construction>
        <Measurements width='data' height='here' />
    </Window>
    """,

    # This XML block is missing the attributes of the <Measurements> tag
    """
    <Window>
        <Label>East0001</Label>
        <Construction>
            <Type>User specified</Type>
        </Construction>
        <Measurements />
    </Window>
    """
]


@pytest.fixture
def sample_window_code() -> typing.Dict[str, code.WindowCode]:
    return {'Code 11': code.WindowCode(
        identifier='Code 11',
        label='202002',
        tags={
            code.WindowCodeTag.GLAZING_TYPE: bilingual.Bilingual(
                english='Double/double with 1 coat',
                french='Double/double, 1 couche',
            ),
            code.WindowCodeTag.COATING_TINTS: bilingual.Bilingual(english='Clear', french='Transparent'),
            code.WindowCodeTag.FILL_TYPE: bilingual.Bilingual(english='6 mm Air', french="6 mm d'air"),
            code.WindowCodeTag.SPACER_TYPE: bilingual.Bilingual(english='Metal', french='Métal'),
            code.WindowCodeTag.CODE_TYPE: bilingual.Bilingual(english='Picture', french='Fixe'),
            code.WindowCodeTag.FRAME_MATERIAL: bilingual.Bilingual(english='Wood', french='Bois'),
        }
    )}


@pytest.fixture
def sample(sample_window_code: typing.Dict[str, code.WindowCode]) -> window.Window:
    return window.Window(
        label='East0001',
        window_code=sample_window_code['Code 11'],
        window_insulation=insulation.Insulation(0.4779),
        width=distance.Distance(1.967738),
        height=distance.Distance(1.3220699),
    )


def test_from_data(raw_sample: element.Element,
                   sample_window_code: typing.Dict[str, code.WindowCode],
                   sample: window.Window) -> None:
    output = window.Window.from_data(raw_sample, sample_window_code)
    assert output == sample


@pytest.mark.parametrize("bad_xml", BAD_XML_DATA)
def test_bad_data(bad_xml: str) -> None:
    window_node = element.Element.from_string(bad_xml)
    with pytest.raises(InvalidEmbeddedDataTypeError) as excinfo:
        window.Window.from_data(window_node, {})

    assert excinfo.value.data_class == window.Window


def test_from_data_missing_codes() -> None:
    doc = """
    <Window>
        <Label>East0001</Label>
        <Construction>
            <Type rValue='0.4779' />
        </Construction>
        <Measurements width='1967.738' height='1322.0699' />
    </Window>
    """
    sample = element.Element.from_string(doc)
    output = window.Window.from_data(sample, {})
    assert output.label == 'East0001'
    assert output.window_code is None
    assert output.to_dict()['glazingTypesEnglish'] is None


def test_to_dict(sample: window.Window) -> None:
    output = sample.to_dict()
    assert output == {
        'label': 'East0001',
        'insulationRsi': 0.4779,
        'insulationR': pytest.approx(2.713642),
        'glazingTypesEnglish': 'Double/double with 1 coat',
        'glazingTypesFrench': 'Double/double, 1 couche',
        'coatingsTintsEnglish': 'Clear',
        'coatingsTintsFrench': 'Transparent',
        'fillTypeEnglish': '6 mm Air',
        'fillTypeFrench': "6 mm d'air",
        'spacerTypeEnglish': 'Metal',
        'spacerTypeFrench': 'Métal',
        'typeEnglish': 'Picture',
        'typeFrench': 'Fixe',
        'frameMaterialEnglish': 'Wood',
        'frameMaterialFrench': 'Bois',
        'areaMetres': pytest.approx(2.601487),
        'areaFeet': pytest.approx(28.002176),
        'widthMetres': 1.967738,
        'widthFeet': pytest.approx(6.455833),
        'heightMetres': 1.3220699,
        'heightFeet': pytest.approx(4.337499),
    }
