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


def test_code_snippet(code: etree.ElementTree) -> None:
    output = snippets.snip_codes(code)
    assert output == {
        'codes': {
            'wall': [{
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
        }
    }
