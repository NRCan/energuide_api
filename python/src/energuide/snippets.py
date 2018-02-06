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


def _wall_snippet(wall: etree.ElementTree) -> typing.Dict[str, typing.Any]:
    label = wall.findtext('Label')

    construction_type_node = wall.find('Construction/Type')
    construction_type_code = construction_type_node.attrib.get('idref') if construction_type_node is not None else None
    nominal_rsi = construction_type_node.attrib['nominalInsulation'] if construction_type_node is not None else None
    effective_rsi = construction_type_node.attrib['rValue'] if construction_type_node is not None else None

    measurements_node = wall.find('Measurements')
    perimeter = measurements_node.attrib['perimeter'] if measurements_node is not None else None
    height = measurements_node.attrib['height'] if measurements_node is not None else None

    return {
        'label': label,
        'constructionTypeCode': construction_type_code,
        'constructionTypeValue': construction_type_node.text,
        'nominalRsi': nominal_rsi,
        'effectiveRsi': effective_rsi,
        'perimeter': perimeter,
        'height': height,
    }


def _door_snippet(door: etree.ElementTree) -> typing.Dict[str, typing.Any]:
    label = door.findtext('Label')
    type_english = door.findtext('Construction/Type/English')
    type_french = door.findtext('Construction/Type/French')

    type_node = door.find('Construction/Type')
    rsi = type_node.attrib['value'] if type_node is not None else None

    measurements_node = door.find('Measurements')
    height = measurements_node.attrib['height'] if measurements_node is not None else None
    width = measurements_node.attrib['width'] if measurements_node is not None else None

    return {
        'label': label,
        'typeEnglish': type_english,
        'typeFrench': type_french,
        'rsi': rsi,
        'height': height,
        'width': width,
    }

def _window_snippet(window: etree.ElementTree) -> typing.Dict[str, typing.Any]:
    label = window.findtext('Label')

    construction_type_node = window.find('Construction/Type')
    construction_type_code = construction_type_node.attrib.get('idref') if construction_type_node is not None else None
    rsi = construction_type_node.attrib['rValue'] if construction_type_node is not None else None

    measurements_node = window.find('Measurements')
    width = measurements_node.attrib['width'] if measurements_node is not None else None
    height = measurements_node.attrib['height'] if measurements_node is not None else None

    return {
        'label': label,
        'constructionTypeCode': construction_type_code,
        'constructionTypeValue': construction_type_node.text,
        'rsi': rsi,
        'width': width,
        'height': height,
    }


def snip_house(house: etree.ElementTree) -> typing.Dict[str, typing.Any]:
    ceilings = house.findall('Components/Ceiling')
    floors = house.findall('Components/Floor')
    walls = house.findall('Components/Wall')
    doors = house.findall('Components/Wall/Components/Door')
    windows = house.findall('Components/*/Components/Window')

    return {
        'ceilings': [_ceiling_snippet(node) for node in ceilings],
        'floors': [_floor_snippet(node) for node in floors],
        'walls': [_wall_snippet(node) for node in walls],
        'doors': [_door_snippet(door) for door in doors],
        'windows': [_window_snippet(node) for node in windows],
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


def _window_code_snippet(window_code: etree.ElementTree) -> typing.Dict[str, typing.Any]:
    code_id = window_code.attrib['id']
    label = window_code.findtext('Label')

    glazing_types_english = window_code.findtext('Layers/GlazingTypes/English')
    glazing_types_french = window_code.findtext('Layers/GlazingTypes/French')

    coatings_tints_english = window_code.findtext('Layers/CoatingsTints/English')
    coatings_tints_french = window_code.findtext('Layers/CoatingsTints/French')

    fill_type_english = window_code.findtext('Layers/FillType/English')
    fill_type_french = window_code.findtext('Layers/FillType/French')

    spacer_type_english = window_code.findtext('Layers/SpacerType/English')
    spacer_type_french = window_code.findtext('Layers/SpacerType/French')

    type_english = window_code.findtext('Layers/Type/English')
    type_french = window_code.findtext('Layers/Type/French')

    frame_material_english = window_code.findtext('Layers/FrameMaterial/English')
    frame_material_french = window_code.findtext('Layers/FrameMaterial/French')

    return {
        'id': code_id,
        'label': label,
        'glazingTypeEnglish': glazing_types_english,
        'glazingTypeFrench': glazing_types_french,
        'coatingsTintsEnglish': coatings_tints_english,
        'coatingsTintsFrench': coatings_tints_french,
        'fillTypeEnglish': fill_type_english,
        'fillTypeFrench': fill_type_french,
        'spacerTypeEnglish': spacer_type_english,
        'spacerTypeFrench': spacer_type_french,
        'typeEnglish': type_english,
        'typeFrench': type_french,
        'frameMaterialEnglish': frame_material_english,
        'frameMaterialFrench': frame_material_french,
    }


def snip_codes(codes: etree.ElementTree) -> typing.Dict[str, typing.Any]:
    wall_codes = codes.findall('Wall/*/Code')
    window_codes = codes.findall('Window/*/Code')

    return {
        'codes': {
            'wall': [_wall_code_snippet(node) for node in wall_codes],
            'window': [_window_code_snippet(node) for node in window_codes],
        }
    }
