import os
from lxml import etree
import pytest
from energuide import snippets


@pytest.fixture
def house() -> etree.ElementTree:
    sample_filename = os.path.join(os.path.dirname(__file__), 'sample.h2k')
    with open(sample_filename, 'r') as h2k:
        doc = etree.parse(h2k)

    house_node = doc.find('House')
    assert house_node is not None
    return house_node


def test_ceiling_snippet(house: etree.ElementTree) -> None:
    output = snippets.snip_house(house)
    assert 'ceilings' in output
    assert len(output['ceilings']) == 2
    assert output['ceilings'][0] == {
        'label': 'Main attic',
        'type_english': 'Attic/gable',
        'type_french': 'Combles/pignon',
        'nominal_rsi': '2.864',
        'effective_rsi': '2.9463',
        'area': '46.4515',
        'length': '23.875',
    }
