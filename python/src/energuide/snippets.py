import typing
from lxml import etree


class _CeilingSnippet(typing.NamedTuple):
    label: typing.Optional[str]
    type_english: typing.Optional[str]
    type_french: typing.Optional[str]
    nominal_rsi: typing.Optional[str]
    effective_rsi: typing.Optional[str]
    area: typing.Optional[str]
    length: typing.Optional[str]


class _FloorSnippet(typing.NamedTuple):
    label: typing.Optional[str]
    nominal_rsi: typing.Optional[str]
    effective_rsi: typing.Optional[str]
    area: typing.Optional[str]
    length: typing.Optional[str]


class _WallSnippet(typing.NamedTuple):
    label: typing.Optional[str]
    construction_type_code: typing.Optional[str]
    construction_type_value: typing.Optional[str]
    nominal_rsi: typing.Optional[str]
    effective_rsi: typing.Optional[str]
    perimeter: typing.Optional[str]
    height: typing.Optional[str]


class _DoorSnippet(typing.NamedTuple):
    label: typing.Optional[str]
    type_english: typing.Optional[str]
    type_french: typing.Optional[str]
    rsi: typing.Optional[str]
    height: typing.Optional[str]
    width: typing.Optional[str]


class _WindowSnippet(typing.NamedTuple):
    label: typing.Optional[str]
    construction_type_code: typing.Optional[str]
    construction_type_value: typing.Optional[str]
    rsi: typing.Optional[str]
    width: typing.Optional[str]
    height: typing.Optional[str]


class _HeatedFloorSnippet(typing.NamedTuple):
    above_grade: typing.Optional[str]
    below_grade: typing.Optional[str]


class _WallCodeSnippet(typing.NamedTuple):
    identifier: str
    label: typing.Optional[str]
    structure_type_english: typing.Optional[str]
    structure_type_french: typing.Optional[str]
    component_type_size_english: typing.Optional[str]
    component_type_size_french: typing.Optional[str]


class _WindowCodeSnippet(typing.NamedTuple):
    identifier: str
    label: typing.Optional[str]
    glazing_types_english: typing.Optional[str]
    glazing_types_french: typing.Optional[str]
    coatings_tints_english: typing.Optional[str]
    coatings_tints_french: typing.Optional[str]
    fill_type_english: typing.Optional[str]
    fill_type_french: typing.Optional[str]
    spacer_type_english: typing.Optional[str]
    spacer_type_french: typing.Optional[str]
    type_english: typing.Optional[str]
    type_french: typing.Optional[str]
    frame_material_english: typing.Optional[str]
    frame_material_french: typing.Optional[str]


class WallCodeSnippet(_WallCodeSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Optional[str]]:
        return {
            'id': self.identifier,
            'label': self.label,
            'structureTypeEnglish': self.structure_type_english,
            'structureTypeFrench': self.structure_type_french,
            'componentTypeSizeEnglish': self.component_type_size_english,
            'componentTypeSizeFrench': self.component_type_size_french,
        }



class WindowCodeSnippet(_WindowCodeSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Optional[str]]:
        return {
            'id': self.identifier,
            'label': self.label,
            'glazingTypesEnglish': self.glazing_types_english,
            'glazingTypesFrench': self.glazing_types_french,
            'coatingsTintsEnglish': self.coatings_tints_english,
            'coatingsTintsFrench': self.coatings_tints_french,
            'fillTypeEnglish': self.fill_type_english,
            'fillTypeFrench': self.fill_type_french,
            'spacerTypeEnglish': self.spacer_type_english,
            'spacerTypeFrench': self.spacer_type_french,
            'typeEnglish': self.type_english,
            'typeFrench': self.type_french,
            'frameMaterialEnglish': self.frame_material_english,
            'frameMaterialFrench': self.frame_material_french,
        }


class _Codes(typing.NamedTuple):
    wall: typing.List[WallCodeSnippet]
    window: typing.List[WindowCodeSnippet]


class Codes(_Codes):

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'codes': {
                'wall': [wall.to_dict() for wall in self.wall],
                'window': [window.to_dict() for window in self.window],
            }
        }


class CeilingSnippet(_CeilingSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Optional[str]]:
        return {
            'label': self.label,
            'typeEnglish': self.type_english,
            'typeFrench': self.type_french,
            'nominalRsi': self.nominal_rsi,
            'effectiveRsi': self.effective_rsi,
            'area': self.area,
            'length': self.length,
        }


class FloorSnippet(_FloorSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Optional[str]]:
        return {
            'label': self.label,
            'nominalRsi': self.nominal_rsi,
            'effectiveRsi': self.effective_rsi,
            'area': self.area,
            'length': self.length,
        }


class WallSnippet(_WallSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Optional[str]]:
        return {
            'label': self.label,
            'constructionTypeCode': self.construction_type_code,
            'constructionTypeValue': self.construction_type_value,
            'nominalRsi': self.nominal_rsi,
            'effectiveRsi': self.effective_rsi,
            'perimeter': self.perimeter,
            'height': self.height,
        }


class DoorSnippet(_DoorSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Optional[str]]:
        return {
            'label': self.label,
            'typeEnglish': self.type_english,
            'typeFrench': self.type_french,
            'rsi': self.rsi,
            'height': self.height,
            'width': self.width,
        }


class WindowSnippet(_WindowSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Optional[str]]:
        return {
            'label': self.label,
            'constructionTypeCode': self.construction_type_code,
            'constructionTypeValue': self.construction_type_value,
            'rsi': self.rsi,
            'width': self.width,
            'height': self.height,
        }


class HeatedFloorSnippet(_HeatedFloorSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Optional[str]]:
        return {
            'aboveGrade': self.above_grade,
            'belowGrade': self.below_grade,
        }


class _HouseSnippet(typing.NamedTuple):
    ceilings: typing.List[CeilingSnippet]
    floors: typing.List[FloorSnippet]
    walls: typing.List[WallSnippet]
    doors: typing.List[DoorSnippet]
    windows: typing.List[WindowSnippet]
    heated_floor_area: HeatedFloorSnippet
    heating_cooling: str
    ventilation: str


class HouseSnippet(_HouseSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'ceilings': [ceiling.to_dict() for ceiling in self.ceilings],
            'floors': [floor.to_dict() for floor in self.floors],
            'walls': [wall.to_dict() for wall in self.walls],
            'doors': [door.to_dict() for door in self.doors],
            'windows': [window.to_dict() for window in self.windows],
            'heatedFloorArea': self.heated_floor_area.to_dict() if self.heated_floor_area is not None else None,
            'heating_cooling': self.heating_cooling,
            'ventilation': self.ventilation,
        }


def _extract_values(node: etree._Element,
                    xpath_mapping: typing.Dict[str, str]) -> typing.Dict[str, typing.Optional[str]]:
    output = {key: node.xpath(value) for key, value in xpath_mapping.items()}
    return {key: value[0] if value else None for key, value in output.items()}


def _ceiling_snippet(ceiling: etree._Element) -> CeilingSnippet:
    return CeilingSnippet(**_extract_values(ceiling, {
        'label': 'Label/text()',
        'type_english': 'Construction/Type/English/text()',
        'type_french': 'Construction/Type/French/text()',
        'nominal_rsi': 'Construction/CeilingType/@nominalInsulation',
        'effective_rsi': 'Construction/CeilingType/@rValue',
        'area': 'Measurements/@area',
        'length': 'Measurements/@length',
    }))


def _floor_snippet(floor: etree._Element) -> FloorSnippet:
    return FloorSnippet(**_extract_values(floor, {
        'label': 'Label/text()',
        'nominal_rsi': 'Construction/Type/@nominalInsulation',
        'effective_rsi': 'Construction/Type/@rValue',
        'area': 'Measurements/@area',
        'length': 'Measurements/@length',
    }))


def _wall_snippet(wall: etree._Element) -> WallSnippet:
    return WallSnippet(**_extract_values(wall, {
        'label': 'Label/text()',
        'construction_type_code': 'Construction/Type/@idref',
        'construction_type_value': 'Construction/Type/text()',
        'nominal_rsi': 'Construction/Type/@nominalInsulation',
        'effective_rsi': 'Construction/Type/@rValue',
        'perimeter': 'Measurements/@perimeter',
        'height': 'Measurements/@height',
    }))


def _door_snippet(door: etree._Element) -> DoorSnippet:
    return DoorSnippet(**_extract_values(door, {
        'label': 'Label/text()',
        'type_english': 'Construction/Type/English/text()',
        'type_french': 'Construction/Type/French/text()',
        'rsi': 'Construction/Type/@value',
        'height': 'Measurements/@height',
        'width': 'Measurements/@width',
    }))


def _window_snippet(window: etree._Element) -> WindowSnippet:
    return WindowSnippet(**_extract_values(window, {
        'label': 'Label/text()',
        'construction_type_code': 'Construction/Type/@idref',
        'construction_type_value': 'Construction/Type/text()',
        'rsi': 'Construction/Type/@rValue',
        'width': 'Measurements/@width',
        'height': 'Measurements/@height',
    }))


def _heated_floor_area_snippet(heated_floor_area: etree._Element) -> HeatedFloorSnippet:
    return HeatedFloorSnippet(**_extract_values(heated_floor_area, {
        'above_grade': '@aboveGrade',
        'below_grade': '@belowGrade',
    }))


def snip_house(house: etree._Element) -> HouseSnippet:
    ceilings = house.xpath('Components/Ceiling')
    floors = house.xpath('Components/Floor')
    walls = house.xpath('Components/Wall')
    doors = house.xpath('Components//Components/Door')
    windows = house.xpath('Components//Components/Window')
    heated_floor_area = house.xpath('Specifications/HeatedFloorArea')
    heating_cooling = house.xpath('HeatingCooling')
    heating_cooling_string = (
        etree.tostring(heating_cooling[0], encoding='unicode') if heating_cooling else None
    )
    ventilation = house.xpath('Ventilation')
    ventilation_string = (
        etree.tostring(ventilation[0], encoding='unicode') if ventilation else None
    )

    return HouseSnippet(
        ceilings=[_ceiling_snippet(node) for node in ceilings],
        floors=[_floor_snippet(node) for node in floors],
        walls=[_wall_snippet(node) for node in walls],
        doors=[_door_snippet(door) for door in doors],
        windows=[_window_snippet(node) for node in windows],
        heated_floor_area=_heated_floor_area_snippet(heated_floor_area[0]) if heated_floor_area else None,
        heating_cooling=heating_cooling_string,
        ventilation=ventilation_string,
    )


def _wall_code_snippet(wall_code: etree._Element) -> WallCodeSnippet:
    return WallCodeSnippet(**_extract_values(wall_code, {
        'identifier': '@id',
        'label': 'Label/text()',
        'structure_type_english': 'Layers/StructureType/English/text()',
        'structure_type_french': 'Layers/StructureType/French/text()',
        'component_type_size_english': 'Layers/ComponentTypeSize/English/text()',
        'component_type_size_french': 'Layers/ComponentTypeSize/French/text()',
    }))


def _window_code_snippet(window_code: etree._Element) -> WindowCodeSnippet:
    return WindowCodeSnippet(**_extract_values(window_code, {
        'identifier': '@id',
        'label': 'Label/text()',
        'glazing_types_english': 'Layers/GlazingTypes/English/text()',
        'glazing_types_french': 'Layers/GlazingTypes/French/text()',
        'coatings_tints_english': 'Layers/CoatingsTints/English/text()',
        'coatings_tints_french': 'Layers/CoatingsTints/French/text()',
        'fill_type_english': 'Layers/FillType/English/text()',
        'fill_type_french': 'Layers/FillType/French/text()',
        'spacer_type_english': 'Layers/SpacerType/English/text()',
        'spacer_type_french': 'Layers/SpacerType/French/text()',
        'type_english': 'Layers/Type/English/text()',
        'type_french': 'Layers/Type/French/text()',
        'frame_material_english': 'Layers/FrameMaterial/English/text()',
        'frame_material_french': 'Layers/FrameMaterial/French/text()',
    }))


def snip_codes(codes: etree._Element
              ) -> Codes:
    wall_codes = codes.xpath('Wall/*/Code')
    window_codes = codes.xpath('Window/*/Code')

    return Codes(
        wall=[_wall_code_snippet(node) for node in wall_codes],
        window=[_window_code_snippet(node) for node in window_codes],
    )
