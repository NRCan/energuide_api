import typing
from energuide import bilingual
from energuide import element
from energuide.exceptions import InvalidEmbeddedDataTypeError, ElementGetValueError


class _WallCode(typing.NamedTuple):
    identifier: str
    label: str
    structure_type: bilingual.Bilingual
    component_type_size: bilingual.Bilingual


class WallCode(_WallCode):

    @classmethod
    def from_data(cls, wall_code: element.Element) -> 'WallCode':
        try:
            return WallCode(
                identifier=wall_code.attrib['id'],
                label=wall_code.get_text('Label'),
                structure_type=bilingual.Bilingual(
                    english=wall_code.get_text('Layers/StructureType/English'),
                    french=wall_code.get_text('Layers/StructureType/French'),
                ),
                component_type_size=bilingual.Bilingual(
                    english=wall_code.get_text('Layers/ComponentTypeSize/English'),
                    french=wall_code.get_text('Layers/ComponentTypeSize/French'),
                )
            )
        except (KeyError, ElementGetValueError) as exc:
            raise InvalidEmbeddedDataTypeError(WallCode) from exc


class _WindowCode(typing.NamedTuple):
    identifier: str
    label: str
    glazing_type: typing.Optional[bilingual.Bilingual]
    coating_tint: typing.Optional[bilingual.Bilingual]
    fill_type: typing.Optional[bilingual.Bilingual]
    spacer_type: typing.Optional[bilingual.Bilingual]
    window_code_type: typing.Optional[bilingual.Bilingual]
    frame_material: typing.Optional[bilingual.Bilingual]


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
                identifier=window_code.attrib['id'],
                label=window_code.get_text('Label'),
                glazing_type=bilingual.Bilingual(
                    english=glazing_type_english,
                    french=glazing_type_french,
                ) if glazing_type_english and glazing_type_french else None,
                coating_tint=bilingual.Bilingual(
                    english=coating_tint_english,
                    french=coating_tint_french,
                ) if coating_tint_english and coating_tint_french else None,
                fill_type=bilingual.Bilingual(
                    english=fill_type_english,
                    french=fill_type_french,
                ) if fill_type_english and fill_type_french else None,
                spacer_type=bilingual.Bilingual(
                    english=spacer_type_english,
                    french=spacer_type_french,
                ) if spacer_type_english and spacer_type_french else None,
                window_code_type=bilingual.Bilingual(
                    english=window_code_type_english,
                    french=window_code_type_french,
                ) if window_code_type_english and window_code_type_french else None,
                frame_material=bilingual.Bilingual(
                    english=frame_material_english,
                    french=frame_material_french,
                ) if frame_material_english and frame_material_french else None,
            )
        except (KeyError, ElementGetValueError) as exc:
            raise InvalidEmbeddedDataTypeError(WindowCode) from exc


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
