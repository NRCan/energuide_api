import typing
from lxml import etree


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


class _HouseSnippet(typing.NamedTuple):
    ceilings: typing.List[str]
    floors: typing.List[str]
    walls: typing.List[str]
    doors: typing.List[str]
    windows: typing.List[str]
    heated_floor_area: str
    heating_cooling: str
    ventilation: typing.List[str]


class HouseSnippet(_HouseSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'ceilings': self.ceilings,
            'floors': self.floors,
            'walls': self.walls,
            'doors': self.doors,
            'windows': self.windows,
            'heatedFloorArea': self.heated_floor_area,
            'heating_cooling': self.heating_cooling,
            'ventilations': self.ventilation,
        }


def _extract_values(node: etree._Element,
                    xpath_mapping: typing.Dict[str, str]) -> typing.Dict[str, typing.Optional[str]]:
    output = {key: node.xpath(value) for key, value in xpath_mapping.items()}
    return {key: value[0] if value else None for key, value in output.items()}


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
    ventilation = house.xpath('Ventilation/WholeHouseVentilatorList/Hrv')
    ventilation_strings = [etree.tostring(hrv, encoding='unicode') for hrv in ventilation]

    return HouseSnippet(
        ceilings=[etree.tostring(node, encoding='unicode') for node in ceilings],
        floors=[etree.tostring(node, encoding='unicode') for node in floors],
        walls=[etree.tostring(node, encoding='unicode') for node in walls],
        doors=[etree.tostring(node, encoding='unicode') for node in doors],
        windows=[etree.tostring(node, encoding='unicode') for node in windows],
        heated_floor_area=etree.tostring(heated_floor_area[0], encoding='unicode') if heated_floor_area else None,
        heating_cooling=heating_cooling_string,
        ventilation=ventilation_strings,
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
