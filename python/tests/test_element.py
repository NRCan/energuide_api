import pytest
from energuide import element


def test_get_text() -> None:
    node = element.Element.from_string('<Foo><Bar>baz</Bar></Foo>')
    assert node.get_text('Bar') == 'baz'


def test_get_text_raises_when_not_found() -> None:
    node = element.Element.from_string('<Foo><Bar>baz</Bar></Foo>')
    with pytest.raises(AssertionError):
        node.get_text('Baz')


def test_xpath_returns_elements() -> None:
    node = element.Element.from_string("<Foo><Bar baz='1' /><Bar baz='2' /></Foo>")
    output = node.xpath('Bar')
    assert len(output) == 2
    assert all([isinstance(bar_node, element.Element) for bar_node in output])
    assert output[0].attrib['baz'] == '1'
