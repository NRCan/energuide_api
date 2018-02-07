import os
from lxml import etree
import pytest
from energuide import snippets


@pytest.fixture
def doc() -> etree.ElementTree:
    sample_filename = os.path.join(os.path.dirname(__file__), 'sample.h2k')
    with open(sample_filename, 'r') as h2k:
        doc = etree.parse(h2k)
    return doc


@pytest.fixture
def house(doc: etree.ElementTree) -> etree.ElementTree:
    house_node = doc.find('House')
    assert house_node is not None
    return house_node


@pytest.fixture
def code(doc: etree.ElementTree) -> etree.ElementTree:
    code_node = doc.find('Codes')
    assert code_node is not None
    return code_node


def test_ceiling_snippet(house: etree.ElementTree) -> None:
    output = snippets.snip_house(house)
    assert 'ceilings' in output
    assert len(output['ceilings']) == 2
    assert output['ceilings'][0] == {
        'label': 'Main attic',
        'typeEnglish': 'Attic/gable',
        'typeFrench': 'Combles/pignon',
        'nominalRsi': '2.864',
        'effectiveRsi': '2.9463',
        'area': '46.4515',
        'length': '23.875',
    }


def test_floor_snippet(house: etree.ElementTree) -> None:
    output = snippets.snip_house(house)
    assert 'floors' in output
    assert len(output['floors']) == 1
    assert output['floors'][0] == {
        'label': 'Rm over garage',
        'nominalRsi': '2.11',
        'effectiveRsi': '2.61',
        'area': '9.2903',
        'length': '3.048',
    }


def test_wall_snippet(house: etree.ElementTree) -> None:
    output = snippets.snip_house(house)
    assert 'walls' in output
    assert len(output['walls']) == 3
    assert sorted(output['walls'], key=lambda row: row['label'])[0] == {
        'label': 'End Wall',
        'constructionTypeCode': 'Code 1',
        'constructionTypeValue': '1201101121',
        'effectiveRsi': '1.7435',
        'nominalRsi': '1.432',
        'perimeter': '7.367',
        'height': '1.2283',
    }

def test_window_snippet(house: etree.ElementTree) -> None:
    output = snippets.snip_house(house)
    assert 'windows' in output
    assert len(output['windows']) == 10
    assert sorted(output['windows'], key=lambda row: row['label'])[0] == {
        'label': 'East0001',
        'constructionTypeCode': 'Code 12',
        'constructionTypeValue': '234002',
        'rsi': '0.4779',
        'height': '1967.738',
        'width': '1322.0699',
    }


def test_heated_floor_area_snippet(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    assert 'heatedFloorArea' in output
    assert output['heatedFloorArea'][0]['aboveGrade'] == '185.8'
    assert output['heatedFloorArea'][0]['belowGrade'] == '92.9'


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
    assert output == {
        'ceilings': [],
        'floors': [],
        'windows': [],
        'walls': [{
            'label': 'Test Floor',
            'constructionTypeCode': None,
            'constructionTypeValue': 'User specified',
            'nominalRsi': '3.3615',
            'effectiveRsi': '2.6892',
            'perimeter': None,
            'height': None,
        }],
        'doors': [],
<<<<<<< HEAD
        'heatedFloorArea': [],
=======
        'heatedFloorArea': None,
>>>>>>> extract heated floor area data
    }


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
    assert len(output['windows']) == 2
    assert len(output['doors']) == 2


def test_wall_code_snippet(code: etree.ElementTree) -> None:
    output = snippets.snip_codes(code)
    assert output['codes']['wall'] == [{
        'id': 'Code 1',
        'label': '1201101121',
        'structureTypeEnglish': 'Wood frame',
        'structureTypeFrench': 'Ossature de bois',
        'componentTypeSizeEnglish': '38x89 mm (2x4 in)',
        'componentTypeSizeFrench': '38x89 (2x4)',
    }, {
        'id': 'Code 2',
        'label': '1201401121',
        'structureTypeEnglish': 'Wood frame',
        'structureTypeFrench': 'Ossature de bois',
        'componentTypeSizeEnglish': '38x89 mm (2x4 in)',
        'componentTypeSizeFrench': '38x89 (2x4)',
    }]


def test_window_code_snippet(code: etree.ElementTree) -> None:
    output = snippets.snip_codes(code)
    assert sorted(output['codes']['window'], key=lambda row: row['label'])[0] == {
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


def test_door_snippet(house: etree.ElementTree) -> None:
    output = snippets.snip_house(house)
    doors_output = sorted(output['doors'], key=lambda x: x['label'])
    assert len(doors_output) == 2
    assert doors_output[0] == {
        'label': 'Back door',
        'typeEnglish': 'Solid wood',
        'typeFrench': 'Bois massif',
        'rsi': '0.39',
        'height': '1.9799',
        'width': '0.8499',
    }
