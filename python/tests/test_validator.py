from lxml import etree
from energuide import validator


def test_validates_xml() -> None:
    raw_xml = '<Foo />'
    doc = etree.fromstring(raw_xml)
    data = {'raw_xml': doc}
    checker = validator.DwellingValidator({'raw_xml': {'type': 'xml'}})
    assert checker.validate(data)


def test_string_fails_validation() -> None:
    raw_xml = '<Foo />'
    data = {'raw_xml': raw_xml}
    checker = validator.DwellingValidator({'raw_xml': {'type': 'xml'}})
    assert not checker.validate(data)


def test_coerce_to_xml() -> None:
    raw_xml = '<Foo />'
    data = {'raw_xml': raw_xml}
    checker = validator.DwellingValidator({'raw_xml': {'type': 'xml', 'coerce': 'parse_xml'}})
    assert checker.validate(data)
    assert isinstance(checker.document['raw_xml'], etree._Element)
