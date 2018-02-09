from energuide import element
from energuide import validator


def test_validates_xml() -> None:
    raw_xml = '<Foo />'
    doc = element.Element.from_string(raw_xml)
    data = {'raw_xml': doc}
    checker = validator.DwellingValidator({'raw_xml': {'type': 'xml', 'required': True}})
    assert checker.validate(data)


def test_string_fails_validation() -> None:
    raw_xml = '<Foo />'
    data = {'raw_xml': raw_xml}
    checker = validator.DwellingValidator({'raw_xml': {'type': 'xml', 'required': True}})
    assert not checker.validate(data)


def test_coerce_to_xml() -> None:
    raw_xml = '<Foo />'
    data = {'raw_xml': raw_xml}
    checker = validator.DwellingValidator({'raw_xml': {'type': 'xml', 'required': True, 'coerce': 'parse_xml'}})
    assert checker.validate(data)
    assert isinstance(checker.document['raw_xml'], element.Element)


def test_embedded_xml() -> None:
    raw_xml = '<Foo />'
    data = {'raw_xml': [raw_xml, raw_xml]}
    schema = {'raw_xml': {'type': 'list', 'required': True, 'schema': {'type': 'xml', 'coerce': 'parse_xml'}}}
    checker = validator.DwellingValidator(schema)
    assert checker.validate(data)
    assert isinstance(checker.document['raw_xml'], list)
    assert len(checker.document['raw_xml']) == 2
    assert isinstance(checker.document['raw_xml'][0], element.Element)
