import py._path.local
import pytest
from energuide import element
from energuide.exceptions import EnerguideError


@pytest.fixture
def fragment() -> str:
    return "<Foo><Bar id='1'>baz</Bar><Bar id='2'>qux</Bar></Foo>"


@pytest.fixture
def fragment_file_path(fragment: str, tmpdir: py._path.local.LocalPath) -> str:
    file = tmpdir.join('data.xml')
    file.write_text('<?xml version="1.0" encoding="UTF-8" ?>', encoding='utf-8')
    file.write_text(fragment, encoding='utf-8')
    return str(file)


@pytest.fixture
def fragment_node(fragment: str) -> element.Element:
    return element.Element.from_string(fragment)


def test_from_string(fragment: str) -> None:
    output = element.Element.from_string(fragment)
    assert isinstance(output, element.Element)
    assert output.tag == 'Foo'


def test_findtext(fragment_node: element.Element) -> None:
    assert fragment_node.findtext('Bar') == 'baz'
    assert fragment_node.findtext('Baz') is None


def test_get_text(fragment_node: element.Element) -> None:
    assert fragment_node.get_text('Bar') == 'baz'


def test_get_text_raises_when_not_found(fragment_node: element.Element) -> None:
    with pytest.raises(AssertionError):
        fragment_node.get_text('Baz')


def test_attrib(fragment_node: element.Element) -> None:
    bar_node = fragment_node.find('Bar')
    assert bar_node
    assert bar_node.attrib['id'] == '1'
    assert 'baz' not in bar_node.attrib


def test_xpath_returns_elements(fragment_node: element.Element) -> None:
    output = fragment_node.xpath('Bar')
    assert len(output) == 2
    assert all([isinstance(bar_node, element.Element) for bar_node in output])
    assert output[0].attrib['id'] == '1'


def test_parse(fragment_file_path: str) -> None:
    with open(fragment_file_path) as xml_file:
        node = element.Element.parse(xml_file)
    assert node.tag == 'Foo'


def test_iter(fragment_node: element.Element) -> None:
    child_nodes = [child for child in fragment_node]
    assert len(child_nodes) == 2
    assert all([isinstance(child, element.Element) for child in child_nodes])
    assert all([child.tag == 'Bar' for child in child_nodes])


def test_find(fragment_node: element.Element) -> None:
    bar_node = fragment_node.find('Bar')
    assert bar_node
    assert bar_node.tag == 'Bar'
    assert bar_node.attrib['id'] == '1'


def test_find_returns_none(fragment_node: element.Element) -> None:
    assert fragment_node.find('Baz') is None


def test_to_string(fragment_node: element.Element) -> None:
    bar_node = fragment_node.find('Bar')
    assert bar_node
    assert bar_node.to_string() == '<Bar id="1">baz</Bar>'


def test_tag(fragment_node: element.Element) -> None:
    assert fragment_node.tag == 'Foo'


def test_new() -> None:
    output = element.Element.new('Foo')
    assert output.tag == 'Foo'


def test_from_malformed_string() -> None:
    with pytest.raises(element.MalformedXmlError):
        element.Element.from_string('</Foo></Foo>')


def test_insert_node() -> None:
    root = element.Element.new('Root')
    child1 = element.Element.new('Child1')
    child2 = element.Element.new('Child2')
    root.insert(0, child1)
    root.insert(0, child2)
    assert len(root.xpath('*')) == 2


def test_get_int(fragment_node: element.Element) -> None:
    assert fragment_node.get('Bar/@id', int) == 1


def test_get_float(fragment_node: element.Element) -> None:
    assert fragment_node.get('Bar/@id', float) == 1.0


def test_get_str(fragment_node: element.Element) -> None:
    assert fragment_node.get('Bar/@id', str) == '1'


def test_get_raises_when_not_found(fragment_node: element.Element) -> None:
    with pytest.raises(EnerguideError):
        fragment_node.get('Bar/@foo', int)


def test_get_raises_when_cant_cast(fragment_node: element.Element) -> None:
    with pytest.raises(EnerguideError):
        fragment_node.get('Bar/text()', int)
