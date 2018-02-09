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
    checker = validator.DwellingValidator({
        'walls': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'walls': output.walls}
    assert checker.validate(doc)


def test_window_snippet(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.windows) == 10
    checker = validator.DwellingValidator({
        'windows': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'windows': output.windows}
    assert checker.validate(doc)


def test_heated_floor_area_snippet(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    checker = validator.DwellingValidator({
        'heated_floor': {'type': 'xml', 'coerce': 'parse_xml'}
    }, allow_unknown=True)
    doc = {'windows': output.heated_floor_area}
    assert checker.validate(doc)


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


def test_wall_code_snippet(code: etree._Element) -> None:
    output = snippets.snip_codes(code)
    assert len(output.wall) == 2
    checker = validator.DwellingValidator({
        'codes': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'codes': output.wall}
    assert checker.validate(doc)


def test_window_code_snippet(code: etree._Element) -> None:
    output = snippets.snip_codes(code)
    assert len(output.wall) == 2
    checker = validator.DwellingValidator({
        'codes': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'codes': output.window}
    assert checker.validate(doc)


def test_door_snippet(house: etree._Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.doors) == 2
    checker = validator.DwellingValidator({
        'doors': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'doors': output.walls}
    assert checker.validate(doc)


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
