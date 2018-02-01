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
        'typeEnglish': 'Attic/gable',
        'typeFrench': 'Combles/pignon',
        'nominalRsi': '2.864',
        'effectiveRsi': '2.9463',
        'area': '46.4515',
        'length': '23.875',
    }

def test_floor_snipped(house: etree.ElementTree) -> None:
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