import typing
from energuide import bilingual
from energuide import element


class _WallCode(typing.NamedTuple):
    identifier: str
    label: str
    structure_type: bilingual.Bilingual
    component_type_size: bilingual.Bilingual


class WallCode(_WallCode):

    @classmethod
    def from_data(cls, wall_code: element.Element) -> 'WallCode':
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


class _WindowCode(typing.NamedTuple):
    identifier: str
    label: str
    glazing_type: bilingual.Bilingual
    coating_tint: bilingual.Bilingual
    fill_type: bilingual.Bilingual
    spacer_type: bilingual.Bilingual
    window_code_type: bilingual.Bilingual
    frame_material: bilingual.Bilingual


class WindowCode(_WindowCode):

    @classmethod
    def from_data(cls, window_code: element.Element) -> 'WindowCode':
        return WindowCode(
            identifier=window_code.attrib['id'],
            label=window_code.get_text('Label'),
            glazing_type=bilingual.Bilingual(
                english=window_code.get_text('Layers/GlazingTypes/English'),
                french=window_code.get_text('Layers/GlazingTypes/French'),
            ),
            coating_tint=bilingual.Bilingual(
                english=window_code.get_text('Layers/CoatingsTints/English'),
                french=window_code.get_text('Layers/CoatingsTints/French'),
            ),
            fill_type=bilingual.Bilingual(
                english=window_code.get_text('Layers/FillType/English'),
                french=window_code.get_text('Layers/FillType/French'),
            ),
            spacer_type=bilingual.Bilingual(
                english=window_code.get_text('Layers/SpacerType/English'),
                french=window_code.get_text('Layers/SpacerType/French'),
            ),
            window_code_type=bilingual.Bilingual(
                english=window_code.get_text('Layers/Type/English'),
                french=window_code.get_text('Layers/Type/French'),
            ),
            frame_material=bilingual.Bilingual(
                english=window_code.get_text('Layers/FrameMaterial/English'),
                french=window_code.get_text('Layers/FrameMaterial/French'),
            )
        )


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
