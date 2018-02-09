import os
from lxml import etree
import pytest
from energuide import snippets
from energuide import validator


@pytest.fixture
def doc() -> etree._ElementTree:
    sample_filename = os.path.join(os.path.dirname(__file__), 'sample.h2k')
    with open(sample_filename, 'r') as h2k:
        doc = etree.parse(h2k)
    return doc


@pytest.fixture
def house(doc: etree._ElementTree) -> etree._Element:
    house_node = doc.find('House')
    assert house_node is not None
    return house_node


@pytest.fixture
def code(doc: etree._ElementTree) -> etree._Element:
    code_node = doc.find('Codes')
    assert code_node is not None
    return code_node


def test_house_snippet_to_dict(house: etree._Element) -> None:
    output = snippets.snip_house(house).to_dict()
    assert len(output) == 8


def test_ceiling_snippet(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.ceilings) == 2
    checker = validator.DwellingValidator({
        'ceilings': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'ceilings': output.ceilings}
    assert checker.validate(doc)


def test_floor_snippet(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.floors) == 1
    checker = validator.DwellingValidator({
        'floors': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'floors': output.floors}
    assert checker.validate(doc)


def test_wall_snippet(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.walls) == 3
    assert sorted(output.walls, key=lambda row: row.label)[0] == snippets.WallSnippet(
        label='End Wall',
        construction_type_code='Code 1',
        construction_type_value='1201101121',
        effective_rsi='1.7435',
        nominal_rsi='1.432',
        perimeter='7.367',
        height='1.2283',
    )


def test_wall_snippet_to_dict(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    assert sorted(output.walls, key=lambda row: row.label)[0].to_dict() == {
        'label': 'End Wall',
        'constructionTypeCode': 'Code 1',
        'constructionTypeValue': '1201101121',
        'effectiveRsi': '1.7435',
        'nominalRsi': '1.432',
        'perimeter': '7.367',
        'height': '1.2283',
    }


def test_window_snippet(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.windows) == 10
    assert sorted(output.windows, key=lambda row: row.label)[0] == snippets.WindowSnippet(
        label='East0001',
        construction_type_code='Code 12',
        construction_type_value='234002',
        rsi='0.4779',
        height='1967.738',
        width='1322.0699',
    )


def test_window_snippet_to_dict(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    assert sorted(output.windows, key=lambda row: row.label)[0].to_dict() == {
        'label': 'East0001',
        'constructionTypeCode': 'Code 12',
        'constructionTypeValue': '234002',
        'rsi': '0.4779',
        'height': '1967.738',
        'width': '1322.0699',
    }


def test_heated_floor_area_snippet(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    assert output.heated_floor_area.above_grade == '185.8'
    assert output.heated_floor_area.below_grade == '92.9'


def test_heated_floor_area_snippet_to_dict(house: etree._Element) -> None:
    output = snippets.snip_house(house).heated_floor_area.to_dict()
    assert output == {
        'aboveGrade': '185.8',
        'belowGrade': '92.9'
    }


def test_user_specified_wall_snippet() -> None:
    xml_text = """
<House><Components>
    <Wall>
        <Label>Test Floor</Label>
        <Construction>
            <Type rValue="2.6892" nominalInsulation="3.3615">User specified</Type>
        </Construction>
    </Wall>
</Components></House>
    """

    doc = etree.fromstring(xml_text)
    output = snippets.snip_house(doc)

    assert output == snippets.HouseSnippet(
        ceilings=[],
        floors=[],
        windows=[],
        walls=[snippets.WallSnippet(
            label='Test Floor',
            construction_type_code=None,
            construction_type_value='User specified',
            nominal_rsi='3.3615',
            effective_rsi='2.6892',
            perimeter=None,
            height=None,
        )],
        doors=[],
        heated_floor_area=None,
        heating_cooling=None,
        ventilation=[],
    )


def test_deeply_embedded_components() -> None:
    xml_text = """
<House><Components>
    <Wall>
        <Label>Test Floor</Label>
        <Construction>
            <Type rValue="2.6892" nominalInsulation="3.3615">User specified</Type>
        </Construction>
        <Components>
            <Door rValue="0.39" adjacentEnclosedSpace="false" id="9">
                <Label>Front door</Label>
                <Construction energyStar="false">
                    <Type code="2" value="0.39">
                        <English>Solid wood</English>
                        <French>Bois massif</French>
                    </Type>
                </Construction>
                <Measurements height="1.9799" width="0.8499" />
                <Components>
                    <Window number="1" er="26.0715" shgc="0.642" frameHeight="1041.4" frameAreaFraction="0.1011" edgeOfGlassFraction="0.1464" centreOfGlassFraction="0.7525" adjacentEnclosedSpace="false" id="14">
                        <Label>East0001</Label>
                        <Construction energyStar="false">
                            <Type rValue="0.4779">User Specified</Type>
                        </Construction>
                        <Measurements height="1967.738" width="1322.0699" headerHeight="2.6396" overhangWidth="0.4115"/>
                    </Window>
                </Components>
            </Door>
        </Components>
    </Wall>
    <Basement>
        <Wall>
            <Label>Test Basement Floor</Label>
            <Construction>
                <Type rValue="2.6892" nominalInsulation="3.3615">User specified</Type>
            </Construction>
            <Components>
                <Door rValue="0.39" adjacentEnclosedSpace="false" id="9">
                    <Label>Back Basemeent door</Label>
                    <Construction energyStar="false">
                        <Type code="2" value="0.39">
                            <English>Solid wood</English>
                            <French>Bois massif</French>
                        </Type>
                    </Construction>
                    <Measurements height="1.9799" width="0.8499" />
                    <Components>
                        <Window number="1" er="26.0715" shgc="0.642" frameHeight="1041.4" frameAreaFraction="0.1011" edgeOfGlassFraction="0.1464" centreOfGlassFraction="0.7525" adjacentEnclosedSpace="false" id="14">
                            <Label>West0001</Label>
                            <Construction energyStar="false">
                                <Type rValue="0.4779">User Specified</Type>
                            </Construction>
                            <Measurements height="1967.738" width="1322.0699" headerHeight="2.6396" overhangWidth="0.4115"/>
                        </Window>
                    </Components>
                </Door>
            </Components>
        </Wall>
    </Basement>
</Components></House>
    """

    doc = etree.fromstring(xml_text)
    output = snippets.snip_house(doc)
    assert len(output.windows) == 2
    assert len(output.doors) == 2


def test_wall_code_snippet_to_dict(code: etree._Element) -> None:
    output = snippets.snip_codes(code)
    assert sorted(output.wall, key=lambda row: row.label)[0].to_dict() == {
        'id': 'Code 1',
        'label': '1201101121',
        'structureTypeEnglish': 'Wood frame',
        'structureTypeFrench': 'Ossature de bois',
        'componentTypeSizeEnglish': '38x89 mm (2x4 in)',
        'componentTypeSizeFrench': '38x89 (2x4)',
    }


def test_wall_code_snippet(code: etree._Element) -> None:
    output = snippets.snip_codes(code)
    assert len(output.wall) == 2
    assert sorted(output.wall, key=lambda row: row.label)[0] == snippets.WallCodeSnippet(
        identifier='Code 1',
        label='1201101121',
        structure_type_english='Wood frame',
        structure_type_french='Ossature de bois',
        component_type_size_english='38x89 mm (2x4 in)',
        component_type_size_french='38x89 (2x4)',
    )


def test_window_code_snippet_to_dict(code: etree._Element) -> None:
    output = snippets.snip_codes(code)
    assert sorted(output.window, key=lambda row: row.label)[0].to_dict() == {
        'id': 'Code 11',
        'label': '202002',
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
    }

def test_window_code_snippet(code: etree._Element) -> None:
    output = snippets.snip_codes(code)
    assert sorted(output.window, key=lambda row: row.label)[0] == snippets.WindowCodeSnippet(
        identifier='Code 11',
        label='202002',
        glazing_types_english='Double/double with 1 coat',
        glazing_types_french='Double/double, 1 couche',
        coatings_tints_english='Clear',
        coatings_tints_french='Transparent',
        fill_type_english='6 mm Air',
        fill_type_french="6 mm d'air",
        spacer_type_english='Metal',
        spacer_type_french='Métal',
        type_english='Picture',
        type_french='Fixe',
        frame_material_english='Wood',
        frame_material_french='Bois',
    )


def test_door_snippet(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    doors_output = sorted(output.doors, key=lambda x: x.label)
    assert len(doors_output) == 2
    assert doors_output[0] == snippets.DoorSnippet(
        label='Back door',
        type_english='Solid wood',
        type_french='Bois massif',
        rsi='0.39',
        height='1.9799',
        width='0.8499',
    )


def test_heating_cooling_snippet(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    doc = etree.fromstring(output.heating_cooling)
    child_tags = {node.tag for node in doc}
    assert 'Label' in child_tags
    assert len(child_tags) == 6


def test_ventilation_snippet(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    doc = etree.fromstring(output.ventilation[0])
    child_tags = {node.tag for node in doc}
    assert 'VentilatorType' in child_tags
    assert len(child_tags) == 3
