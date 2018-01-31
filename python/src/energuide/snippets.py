import typing
from xml.etree import ElementTree


def _ceiling_snippet(ceiling: ElementTree) -> typing.Dict[str, typing.Any]:
    label = ceiling.findtext('Label')
    type_english = ceiling.findtext('Construction/Type/English')
    type_french = ceiling.findtext('Construction/Type/French')

    nominal_rsi_node = ceiling.find('Construction/CeilingType')
    nominal_rsi = nominal_rsi_node.attrib['nominalInsulation'] if nominal_rsi_node is not None else None
    effective_rsi_node = ceiling.find('Construction/CeilingType')
    effective_rsi = effective_rsi_node.attrib['rValue'] if effective_rsi_node is not None else None
    return {
        'label': label,
        'type_english': type_english,
        'type_french': type_french,
        'nominal_rsi': nominal_rsi,
        'effective_rsi': effective_rsi,
    }


def snip_house(house: ElementTree) -> typing.Dict[str, typing.Any]:
    ceilings = house.findall('Components/Ceiling')
    return {
        'ceilings': [_ceiling_snippet(node) for node in ceilings]
    }
