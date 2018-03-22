import typing
import cerberus
from energuide import element


class DwellingValidator(cerberus.Validator):

    def _validate_type_xml(self, value: typing.Any) -> bool:  # pylint: disable=no-self-use
        return isinstance(value, element.Element)

    def _normalize_coerce_parse_xml(self, value: typing.Any) -> element.Element:  # pylint: disable=no-self-use
        assert isinstance(value, str), "Can't coerce non-strings to XML"
        return element.Element.from_string(value)
