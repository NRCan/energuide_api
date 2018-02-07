import typing
from lxml import etree


def _extract_values(node: etree._Element,
                    xpath_mapping: typing.Dict[str, str]) -> typing.Dict[str, typing.Optional[str]]:
    output = {key: node.xpath(value) for key, value in xpath_mapping.items()}
    return {key: value[0] if value else None for key, value in output.items()}


def _ceiling_snippet(ceiling: etree._Element) -> typing.Dict[str, typing.Optional[str]]:
    return _extract_values(ceiling, {
        'label': 'Label/text()',
        'typeEnglish': 'Construction/Type/English/text()',
        'typeFrench': 'Construction/Type/French/text()',
        'nominalRsi': 'Construction/CeilingType/@nominalInsulation',
        'effectiveRsi': 'Construction/CeilingType/@rValue',
        'area': 'Measurements/@area',
        'length': 'Measurements/@length',
    })


def _floor_snippet(floor: etree._Element) -> typing.Dict[str, typing.Optional[str]]:
    return _extract_values(floor, {
        'label': 'Label/text()',
        'nominalRsi': 'Construction/Type/@nominalInsulation',
        'effectiveRsi': 'Construction/Type/@rValue',
        'area': 'Measurements/@area',
        'length': 'Measurements/@length',
    })


def _wall_snippet(wall: etree._Element) -> typing.Dict[str, typing.Optional[str]]:
    return _extract_values(wall, {
        'label': 'Label/text()',
        'constructionTypeCode': 'Construction/Type/@idref',
        'constructionTypeValue': 'Construction/Type/text()',
        'nominalRsi': 'Construction/Type/@nominalInsulation',
        'effectiveRsi': 'Construction/Type/@rValue',
        'perimeter': 'Measurements/@perimeter',
        'height': 'Measurements/@height',
    })


def _door_snippet(door: etree._Element) -> typing.Dict[str, typing.Optional[str]]:
    return _extract_values(door, {
        'label': 'Label/text()',
        'typeEnglish': 'Construction/Type/English/text()',
        'typeFrench': 'Construction/Type/French/text()',
        'rsi': 'Construction/Type/@value',
        'height': 'Measurements/@height',
        'width': 'Measurements/@width',
    })


def _window_snippet(window: etree._Element) -> typing.Dict[str, typing.Optional[str]]:
    return _extract_values(window, {
        'label': 'Label/text()',
        'constructionTypeCode': 'Construction/Type/@idref',
        'constructionTypeValue': 'Construction/Type/text()',
        'rsi': 'Construction/Type/@rValue',
        'width': 'Measurements/@width',
        'height': 'Measurements/@height',
    })


def _heated_floor_area_snippet(heated_floor_area: etree._Element) -> typing.Dict[str, typing.Optional[str]]:
    return _extract_values(heated_floor_area, {
        'aboveGrade': '@aboveGrade',
        'belowGrade': '@belowGrade',
    })


def snip_house(house: etree._Element) -> typing.Dict[str, typing.List[typing.Dict[str, typing.Optional[str]]]]:
    ceilings = house.xpath('Components/Ceiling')
    floors = house.xpath('Components/Floor')
    walls = house.xpath('Components/Wall')
    doors = house.xpath('Components//Components/Door')
    windows = house.xpath('Components//Components/Window')
    heated_floor_areas = house.xpath('Specifications/HeatedFloorArea')

    return {
        'ceilings': [_ceiling_snippet(node) for node in ceilings],
        'floors': [_floor_snippet(node) for node in floors],
        'walls': [_wall_snippet(node) for node in walls],
        'doors': [_door_snippet(door) for door in doors],
        'windows': [_window_snippet(node) for node in windows],
        'heatedFloorArea': [_heated_floor_area_snippet(heated_floor_area) for heated_floor_area in heated_floor_areas],
    }


def _wall_code_snippet(wall_code: etree._Element) -> typing.Dict[str, typing.Optional[str]]:
    return _extract_values(wall_code, {
        'id': '@id',
        'label': 'Label/text()',
        'structureTypeEnglish': 'Layers/StructureType/English/text()',
        'structureTypeFrench': 'Layers/StructureType/French/text()',
        'componentTypeSizeEnglish': 'Layers/ComponentTypeSize/English/text()',
        'componentTypeSizeFrench': 'Layers/ComponentTypeSize/French/text()',
    })


def _window_code_snippet(window_code: etree._Element) -> typing.Dict[str, typing.Optional[str]]:
    return _extract_values(window_code, {
        'id': '@id',
        'label': 'Label/text()',
        'glazingTypesEnglish': 'Layers/GlazingTypes/English/text()',
        'glazingTypesFrench': 'Layers/GlazingTypes/French/text()',
        'coatingsTintsEnglish': 'Layers/CoatingsTints/English/text()',
        'coatingsTintsFrench': 'Layers/CoatingsTints/French/text()',
        'fillTypeEnglish': 'Layers/FillType/English/text()',
        'fillTypeFrench': 'Layers/FillType/French/text()',
        'spacerTypeEnglish': 'Layers/SpacerType/English/text()',
        'spacerTypeFrench': 'Layers/SpacerType/French/text()',
        'typeEnglish': 'Layers/Type/English/text()',
        'typeFrench': 'Layers/Type/French/text()',
        'frameMaterialEnglish': 'Layers/FrameMaterial/English/text()',
        'frameMaterialFrench': 'Layers/FrameMaterial/French/text()',
    })


def snip_codes(codes: etree._Element
              ) -> typing.Dict[str, typing.Dict[str, typing.List[typing.Dict[str, typing.Optional[str]]]]]:
    wall_codes = codes.xpath('Wall/*/Code')
    window_codes = codes.xpath('Window/*/Code')

    return {
        'codes': {
            'wall': [_wall_code_snippet(node) for node in wall_codes],
            'window': [_window_code_snippet(node) for node in window_codes],
        }
    }
