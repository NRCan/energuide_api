import enum
import typing
from energuide import bilingual
from energuide import element
from energuide.exceptions import InvalidEmbeddedDataTypeError, ElementGetValueError


class WallCodeTag(enum.Enum):
    STRUCTURE_TYPE = enum.auto()
    COMPONENT_TYPE_SIZE = enum.auto()


class _WallCode(typing.NamedTuple):
    identifier: str
    label: str
    tags: typing.Dict[WallCodeTag, typing.Optional[bilingual.Bilingual]]


class WallCode(_WallCode):

    @classmethod
    def from_data(cls, wall_code: element.Element) -> 'WallCode':
        structure_type_english = wall_code.findtext('Layers/StructureType/English')
        structure_type_french = wall_code.findtext('Layers/StructureType/French')

        component_type_size_english = wall_code.findtext('Layers/ComponentTypeSize/English')
        component_type_size_french = wall_code.findtext('Layers/ComponentTypeSize/French')

        try:
            return WallCode(
                identifier=wall_code.get('@id', str),
                label=wall_code.get_text('Label'),
                tags={
                    WallCodeTag.STRUCTURE_TYPE: bilingual.Bilingual(
                        english=structure_type_english,
                        french=structure_type_french,
                    ) if structure_type_english and structure_type_french else None,
                    WallCodeTag.COMPONENT_TYPE_SIZE: bilingual.Bilingual(
                        english=component_type_size_english,
                        french=component_type_size_french,
                    ) if component_type_size_english and component_type_size_french else None,
                }
            )
        except ElementGetValueError as exc:
            raise InvalidEmbeddedDataTypeError(WallCode, 'Unable to get identifier attributes') from exc


class WindowCodeTag(enum.Enum):
    GLAZING_TYPE = enum.auto()
    COATING_TINTS = enum.auto()
    FILL_TYPE = enum.auto()
    SPACER_TYPE = enum.auto()
    CODE_TYPE = enum.auto()
    FRAME_MATERIAL = enum.auto()


class _WindowCode(typing.NamedTuple):
    identifier: str
    label: str
    tags: typing.Dict[WindowCodeTag, typing.Optional[bilingual.Bilingual]]


class WindowCode(_WindowCode):

    @classmethod
    def from_data(cls, window_code: element.Element) -> 'WindowCode':

        glazing_type_english = window_code.findtext('Layers/GlazingTypes/English')
        glazing_type_french = window_code.findtext('Layers/GlazingTypes/French')

        coating_tint_english = window_code.findtext('Layers/CoatingsTints/English')
        coating_tint_french = window_code.findtext('Layers/CoatingsTints/French')

        fill_type_english = window_code.findtext('Layers/FillType/English')
        fill_type_french = window_code.findtext('Layers/FillType/French')

        spacer_type_english = window_code.findtext('Layers/SpacerType/English')
        spacer_type_french = window_code.findtext('Layers/SpacerType/French')

        window_code_type_english = window_code.findtext('Layers/Type/English')
        window_code_type_french = window_code.findtext('Layers/Type/French')

        frame_material_english = window_code.findtext('Layers/FrameMaterial/English')
        frame_material_french = window_code.findtext('Layers/FrameMaterial/French')

        try:
            return WindowCode(
                identifier=window_code.get('@id', str),
                label=window_code.get_text('Label'),
                tags={
                    WindowCodeTag.GLAZING_TYPE: bilingual.Bilingual(
                        english=glazing_type_english,
                        french=glazing_type_french,
                    ) if glazing_type_english and glazing_type_french else None,
                    WindowCodeTag.COATING_TINTS: bilingual.Bilingual(
                        english=coating_tint_english,
                        french=coating_tint_french,
                    ) if coating_tint_english and coating_tint_french else None,
                    WindowCodeTag.FILL_TYPE: bilingual.Bilingual(
                        english=fill_type_english,
                        french=fill_type_french,
                    ) if fill_type_english and fill_type_french else None,
                    WindowCodeTag.SPACER_TYPE: bilingual.Bilingual(
                        english=spacer_type_english,
                        french=spacer_type_french,
                    ) if spacer_type_english and spacer_type_french else None,
                    WindowCodeTag.CODE_TYPE: bilingual.Bilingual(
                        english=window_code_type_english,
                        french=window_code_type_french,
                    ) if window_code_type_english and window_code_type_french else None,
                    WindowCodeTag.FRAME_MATERIAL: bilingual.Bilingual(
                        english=frame_material_english,
                        french=frame_material_french,
                    ) if frame_material_english and frame_material_french else None,
                }
            )
        except ElementGetValueError as exc:
            raise InvalidEmbeddedDataTypeError(WindowCode, 'Unable to get identifier attributes') from exc


class _Codes(typing.NamedTuple):
    wall: typing.Dict[str, WallCode]
    window: typing.Dict[str, WindowCode]


class Codes(_Codes):

    @classmethod
    def from_data(cls, codes: typing.Dict[str, typing.List[element.Element]]) -> 'Codes':
        wall_code_list = [WallCode.from_data(wall_code) for wall_code in codes['wall']]
        window_code_list = [WindowCode.from_data(window_code) for window_code in codes['window']]

        wall_codes = {wall_code.identifier: wall_code for wall_code in wall_code_list}
        window_codes = {window_code.identifier: window_code for window_code in window_code_list}

        return Codes(
            wall=wall_codes,
            window=window_codes,
        )
