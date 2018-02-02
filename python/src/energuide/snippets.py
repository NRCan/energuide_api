import typing
from lxml import etree


def _ceiling_snippet(ceiling: etree.ElementTree) -> typing.Dict[str, typing.Any]:
    label = ceiling.findtext('Label')
    type_english = ceiling.findtext('Construction/Type/English')
    type_french = ceiling.findtext('Construction/Type/French')

    nominal_rsi_node = ceiling.find('Construction/CeilingType')
    nominal_rsi = nominal_rsi_node.attrib['nominalInsulation'] if nominal_rsi_node is not None else None
    effective_rsi_node = ceiling.find('Construction/CeilingType')
    effective_rsi = effective_rsi_node.attrib['rValue'] if effective_rsi_node is not None else None
    measurements_node = ceiling.find('Measurements')
    area = measurements_node.attrib['area'] if measurements_node is not None else None
    length = measurements_node.attrib['length'] if measurements_node is not None else None
    return {
        'label': label,
        'typeEnglish': type_english,
        'typeFrench': type_french,
        'nominalRsi': nominal_rsi,
        'effectiveRsi': effective_rsi,
        'area': area,
        'length': length,
    }


def _floor_snippet(floor: etree.ElementTree) -> typing.Dict[str, typing.Any]:
    label = floor.findtext('Label')

    rsi_node = floor.find('Construction/Type')
    nominal_rsi = rsi_node.attrib['nominalInsulation'] if rsi_node is not None else None
    effective_rsi = rsi_node.attrib['rValue'] if rsi_node is not None else None
    measurements_node = floor.find('Measurements')
    area = measurements_node.attrib['area']
    length = measurements_node.attrib['length']

    return {
        'label': label,
        'nominalRsi': nominal_rsi,
        'effectiveRsi': effective_rsi,
        'area': area,
        'length': length,
    }


def snip_house(house: etree.ElementTree) -> typing.Dict[str, typing.Any]:
    ceilings = house.findall('Components/Ceiling')
    floors = house.findall('Components/Floor')
    return {
        'ceilings': [_ceiling_snippet(node) for node in ceilings],
        'floors': [_floor_snippet(node) for node in floors],
    }


def _wall_code_snippet(wall_code: etree.ElementTree) -> typing.Dict[str, typing.Any]:
    code_id = wall_code.attrib['id']
    label = wall_code.findtext('Label')
    structure_type_english = wall_code.findtext('Layers/StructureType/English')
    structure_type_french = wall_code.findtext('Layers/StructureType/French')
    component_type_size_english = wall_code.findtext('Layers/ComponentTypeSize/English')
    component_type_size_french = wall_code.findtext('Layers/ComponentTypeSize/French')

    return {
        'id': code_id,
        'label': label,
        'structureTypeEnglish': structure_type_english,
        'structureTypeFrench': structure_type_french,
        'componentTypeSizeEnglish': component_type_size_english,
        'componentTypeSizeFrench': component_type_size_french,
    }


def snip_codes(codes: etree.ElementTree) -> typing.Dict[str, typing.Any]:
    wall_codes = codes.findall('Wall/*/Code')

    return {
        'codes': {
            'wall': [_wall_code_snippet(node) for node in wall_codes]
        }
    }
