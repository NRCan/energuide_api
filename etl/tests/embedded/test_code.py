import typing
import pytest
from energuide import bilingual
from energuide import element
from energuide.embedded import code
from energuide.exceptions import InvalidEmbeddedDataTypeError


@pytest.fixture
def raw_wall_code() -> element.Element:
    data = """
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
"""
    return element.Element.from_string(data)


BAD_WALL_CODE_XML = [
    # This XML block is missing the id attribute on the <Code> tag
    """
<Code>
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

    # This XML block is missing the <StructureType> tag
    """
<Code id='Code 1'>
    <Label>1201101121</Label>
    <Layers>
        <ComponentTypeSize>
            <English>38x89 mm (2x4 in)</English>
            <French>38x89 (2x4)</French>
        </ComponentTypeSize>
    </Layers>
</Code>
    """,
]


BAD_WINDOW_CODE_XML = [
    # This XML block is missing the id attribute on the <Code> tag
    """
<Code>
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

    # This XML block is missing all the tags under <Layers>
    """
<Code id='Code 11'>
    <Label>202002</Label>
    <Layers>
    </Layers>
</Code>
    """,
]


@pytest.fixture
def wall_code() -> code.WallCode:
    return code.WallCode(
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


@pytest.fixture
def raw_window_code() -> element.Element:
    data = """
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
"""
    return element.Element.from_string(data)


@pytest.fixture
def window_code() -> code.WindowCode:
    return code.WindowCode(
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


@pytest.fixture
def raw_codes(raw_wall_code: element.Element,
              raw_window_code: element.Element) -> typing.Dict[str, typing.List[element.Element]]:
    return {
        'wall': [raw_wall_code],
        'window': [raw_window_code],
    }


def test_wall_code_from_data(raw_wall_code: element.Element, wall_code: code.WallCode) -> None:
    output = code.WallCode.from_data(raw_wall_code)
    assert output == wall_code


def test_window_code_from_data(raw_window_code: element.Element, window_code: code.WindowCode) -> None:
    output = code.WindowCode.from_data(raw_window_code)
    assert output == window_code


@pytest.mark.parametrize("bad_xml", BAD_WALL_CODE_XML)
def test_bad_wall_code(bad_xml: str) -> None:
    code_node = element.Element.from_string(bad_xml)
    with pytest.raises(InvalidEmbeddedDataTypeError) as excinfo:
        code.WallCode.from_data(code_node)

    assert excinfo.value.data_class == code.WallCode


@pytest.mark.parametrize("bad_xml", BAD_WINDOW_CODE_XML)
def test_bad_window_code(bad_xml: str) -> None:
    code_node = element.Element.from_string(bad_xml)
    with pytest.raises(InvalidEmbeddedDataTypeError) as excinfo:
        code.WindowCode.from_data(code_node)

    assert excinfo.value.data_class == code.WindowCode


def test_code_from_data(raw_wall_code: element.Element,
                        raw_window_code: element.Element,
                        wall_code: code.WallCode,
                        window_code: code.WindowCode) -> None:
    output = code.Codes.from_data(
        {'wall': [raw_wall_code], 'window': [raw_window_code]}
    )
    assert output == code.Codes(
        wall={wall_code.identifier: wall_code},
        window={window_code.identifier: window_code}
    )
