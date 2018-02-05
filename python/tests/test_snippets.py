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
        'walls': [{
            'label': 'Test Floor',
            'constructionTypeCode': None,
            'constructionTypeValue': 'User specified',
            'nominalRsi': '3.3615',
            'effectiveRsi': '2.6892',
            'perimeter': None,
            'height': None,
        }]
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
            }],
            'window': [{
                'id': 'Code 11',
                'label': '202002',
                'glazingTypeEnglish': 'Double/double with 1 coat',
                'glazingTypeFrench': 'Double/double, 1 couche',
                'coatingsTintsEnglish': 'Clear',
                'coatingsTintsFrench': 'Transparent',
                'fillTypeEnglish': '6 mm Air',
                'fillTypeFrench': '6 mm d\'air',
                'spacerTypeEnglish': 'Metal',
                'spacerTypeFrench': 'Métal',
                'typeEnglish': 'Picture',
                'typeFrench': 'Fixe',
                'frameMaterialEnglish': 'Wood',
                'frameMaterialFrench': 'Bois',
            },
            {
                'id': 'Code 12',
                'label': '234002',
                'glazingTypeEnglish': 'Double/double with 1 coat',
                'glazingTypeFrench': 'Double/double, 1 couche',
                'coatingsTintsEnglish': 'Low-E .20 (hard1)',
                'coatingsTintsFrench': 'Faible E .20 (Dur 1)',
                'fillTypeEnglish': '9 mm Argon',
                'fillTypeFrench': '9 mm d\'argon',
                'spacerTypeEnglish': 'Metal',
                'spacerTypeFrench': 'Métal',
                'typeEnglish': 'Picture',
                'typeFrench': 'Fixe',
                'frameMaterialEnglish': 'Wood',
                'frameMaterialFrench': 'Bois',
            },
            {
                'id': 'Code 13',
                'label': '330204',
                'glazingTypeEnglish': 'Triple/triple with 1 coat',
                'glazingTypeFrench': 'Triple/triple, 1 couche',
                'coatingsTintsEnglish': 'Low-E .20 (hard1)',
                'coatingsTintsFrench': 'Faible E .20 (Dur 1)',
                'fillTypeEnglish': '13 mm Air',
                'fillTypeFrench': '13 mm d\'air',
                'spacerTypeEnglish': 'Insulating',
                'spacerTypeFrench': 'Isolant',
                'typeEnglish': 'Picture',
                'typeFrench': 'Fixe',
                'frameMaterialEnglish': 'Vinyl',
                'frameMaterialFrench': 'Vinyle',
            },
            {
                'id': 'Code 14',
                'label': '334006',
                'glazingTypeEnglish': 'Triple/triple with 1 coat',
                'glazingTypeFrench': 'Triple/triple, 1 couche',
                'coatingsTintsEnglish': 'Low-E .20 (hard1)',
                'coatingsTintsFrench': 'Faible E .20 (Dur 1)',
                'fillTypeEnglish': '9 mm Argon',
                'fillTypeFrench': '9 mm d\'argon',
                'spacerTypeEnglish': 'Metal',
                'spacerTypeFrench': 'Métal',
                'typeEnglish': 'Picture',
                'typeFrench': 'Fixe',
                'frameMaterialEnglish': 'Fibreglass',
                'frameMaterialFrench': 'Fibre de verre',
            }],
        }
    }