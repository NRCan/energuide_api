import typing
import cerberus
from lxml import etree


class DwellingValidator(cerberus.Validator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')

    def _validate_type_xml(self, value: typing.Any) -> bool:  # pylint: disable=no-self-use
        return isinstance(value, etree._Element)

    def _normalize_coerce_parse_xml(self, value: typing.Any) -> typing.Optional[etree._Element]:
        assert isinstance(value, str), "Can't coerce non-strings to XML"
        return etree.fromstring(value.encode('utf-8'), self._parser)
