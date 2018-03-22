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


def test_energy_snippet_to_dict(doc: element.Element) -> None:
    output = snippets.snip_energy_upgrade_order(doc).to_dict()
    assert len(output) == 1


def test_upgrades_snippet(doc: element.Element) -> None:
    output = snippets.snip_energy_upgrade_order(doc)
    assert len(output.upgrades) == 12
    checker = validator.DwellingValidator({
        'upgrades': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}
    }, allow_unknown=True)

    document = {'upgrades': output.upgrades}
    assert checker.validate(document)
