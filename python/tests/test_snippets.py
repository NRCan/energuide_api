import os
from xml.etree import ElementTree
import pytest
from energuide import snippets


@pytest.fixture
def house() -> ElementTree:
    sample_filename = os.path.join(os.path.dirname(__file__), 'sample.h2k')
    with open(sample_filename, 'r') as h2k:
        doc = ElementTree.parse(h2k)

    house_node = doc.find('House')
    assert house_node
    return house_node


def test_ceiling_snippet(house: ElementTree) -> None:
    output = snippets.snip_house(house)
    assert 'ceilings' in output
    assert len(output['ceilings']) == 2
    assert output['ceilings'][0]['nominal_rsi'] == '2.864'
