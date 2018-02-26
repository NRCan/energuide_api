import os
import pytest
from energuide import element
from energuide import snippets
from energuide import validator


@pytest.fixture
def doc() -> element.Element:
    sample_filename = os.path.join(os.path.dirname(__file__), 'sample.h2k')
    with open(sample_filename, 'r') as h2k:
        doc = element.Element.parse(h2k)
    return doc


@pytest.fixture
def house(doc: element.Element) -> element.Element:
    house_node = doc.find('House')
    assert house_node is not None
    return house_node


@pytest.fixture
def code(doc: element.Element) -> element.Element:
    code_node = doc.find('Codes')
    assert code_node is not None
    return code_node


@pytest.fixture
def energy_upgrades(doc: element.Element) -> element.Element:
    energy_upgrades_node = doc.find('EnergyUpgrades')
    assert energy_upgrades_node is not None
    return energy_upgrades_node


def test_house_snippet_to_dict(house: element.Element) -> None:
    output = snippets.snip_house(house).to_dict()
    assert len(output) == 12


def test_energy_snippet_to_dict(energy_upgrades: element.Element) -> None:
    output = snippets.snip_energy_upgrades(energy_upgrades).to_dict()
    assert len(output) == 1


def test_ceiling_snippet(house: element.Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.ceilings) == 2
    checker = validator.DwellingValidator({
        'ceilings': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'ceilings': output.ceilings}
    assert checker.validate(doc)


def test_floor_snippet(house: element.Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.floors) == 1
    checker = validator.DwellingValidator({
        'floors': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'floors': output.floors}
    assert checker.validate(doc)


def test_wall_snippet(house: element.Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.walls) == 3
    checker = validator.DwellingValidator({
        'walls': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'walls': output.walls}
    assert checker.validate(doc)


def test_window_snippet(house: element.Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.windows) == 10
    checker = validator.DwellingValidator({
        'windows': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'windows': output.windows}
    assert checker.validate(doc)


def test_heated_floor_area_snippet(house: element.Element) -> None:
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

    doc = element.Element.from_string(xml_text)
    output = snippets.snip_house(doc)
    assert len(output.windows) == 2
    assert len(output.doors) == 2


def test_wall_code_snippet(code: element.Element) -> None:
    output = snippets.snip_codes(code)
    assert len(output.wall) == 2
    checker = validator.DwellingValidator({
        'codes': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'codes': output.wall}
    assert checker.validate(doc)


def test_window_code_snippet(code: element.Element) -> None:
    output = snippets.snip_codes(code)
    assert len(output.wall) == 2
    checker = validator.DwellingValidator({
        'codes': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'codes': output.window}
    assert checker.validate(doc)


def test_door_snippet(house: element.Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.doors) == 2
    checker = validator.DwellingValidator({
        'doors': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'doors': output.walls}
    assert checker.validate(doc)


def test_heating_cooling_snippet(house: element.Element) -> None:
    output = snippets.snip_house(house)
    assert output.heating_cooling
    doc = element.Element.from_string(output.heating_cooling)
    child_tags = {node.tag for node in doc}
    assert 'Label' in child_tags
    assert len(child_tags) == 6


def test_ventilation_snippet(house: element.Element) -> None:
    output = snippets.snip_house(house)
    doc = element.Element.from_string(output.ventilation[0])
    child_tags = {node.tag for node in doc}
    assert 'VentilatorType' in child_tags
    assert len(child_tags) == 3


def test_water_heating_snippet(house: element.Element) -> None:
    output = snippets.snip_house(house)
    assert output.water_heating
    doc = element.Element.from_string(output.water_heating)
    nodes = doc.xpath('*[self::Primary or self::Secondary]')
    assert len(nodes) == 2

    assert all([water_heating.attrib['hasDrainWaterHeatRecovery'] == 'false'
                for water_heating in nodes])


def test_basement_snippet(house: element.Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.basements) == 1
    checker = validator.DwellingValidator({
        'basements': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'basements': output.basements}
    assert checker.validate(doc)


def test_crawlspace_snippet(house: element.Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.crawlspaces) == 1
    checker = validator.DwellingValidator({
        'crawlspaces': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'crawlspaces': output.crawlspaces}
    assert checker.validate(doc)


def test_slab_snippet(house: element.Element) -> None:
    output = snippets.snip_house(house)
    assert len(output.slabs) == 1
    checker = validator.DwellingValidator({
        'slabs': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)
    doc = {'slabs': output.crawlspaces}
    assert checker.validate(doc)


def test_upgrades_snuppet(energy_upgrades: element.Element) -> None:
    output = snippets.snip_energy_upgrades(energy_upgrades)
    assert len(output.upgrades) == 12
    checker = validator.DwellingValidator({
        'upgrades': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)

    doc = {'upgrades': output.upgrades}
    assert checker.validate(doc)

