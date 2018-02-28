import typing
from energuide.embedded import area
from energuide.embedded import code
from energuide.embedded import insulation
from energuide.embedded import distance
from energuide import element
from energuide.exceptions import InvalidEmbeddedDataTypeError, ElementGetValueError


_MILLIMETRES_TO_METRES = 1000


class _Window(typing.NamedTuple):
    label: str
    window_code: typing.Optional[code.WindowCode]
    window_insulation: insulation.Insulation
    width: distance.Distance
    height: distance.Distance


class Window(_Window):

    _CODE_TAG_TRANSLATIONS = [
        (code.WindowCodeTag.GLAZING_TYPE, 'glazingTypes'),
        (code.WindowCodeTag.COATING_TINTS, 'coatingsTints'),
        (code.WindowCodeTag.FILL_TYPE, 'fillType'),
        (code.WindowCodeTag.SPACER_TYPE, 'spacerType'),
        (code.WindowCodeTag.CODE_TYPE, 'type'),
        (code.WindowCodeTag.FRAME_MATERIAL, 'frameMaterial'),
    ]

    @classmethod
    def from_data(cls,
                  window: element.Element,
                  window_codes: typing.Dict[str, code.WindowCode]) -> 'Window':

        code_id = window.xpath('Construction/Type/@idref')
        window_code = window_codes[code_id[0]] if code_id else None

        try:
            return Window(
                label=window.get_text('Label'),
                window_code=window_code,
                window_insulation=insulation.Insulation(window.get('Construction/Type/@rValue', float)),
                width=distance.Distance(window.get('Measurements/@width', float) / _MILLIMETRES_TO_METRES),
                height=distance.Distance(window.get('Measurements/@height', float) / _MILLIMETRES_TO_METRES),
            )
        except (ElementGetValueError) as exc:
            raise InvalidEmbeddedDataTypeError(Window) from exc

    @property
    def _window_area(self) -> area.Area:
        return area.Area(self.width.metres * self.height.metres)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        code_tags: typing.Dict[str, typing.Optional[str]] = dict(
            item
            for _, tag_name in self._CODE_TAG_TRANSLATIONS
            for item in {
                f'{tag_name}English': None,
                f'{tag_name}French': None,
            }.items()
        )

        if self.window_code:
            for tag_type, tag_name in self._CODE_TAG_TRANSLATIONS:
                tag_value = self.window_code.tags.get(tag_type)
                code_tags.update(
                    **{
                        f'{tag_name}English': tag_value.english if tag_value else None,
                        f'{tag_name}French': tag_value.french if tag_value else None,
                    }
                )

        return {
            'label': self.label,
            'insulationRsi': self.window_insulation.rsi,
            'insulationR': self.window_insulation.r_value,
            **code_tags,
            'areaMetres': self._window_area.square_metres,
            'areaFeet': self._window_area.square_feet,
            'widthMetres': self.width.metres,
            'widthFeet': self.width.feet,
            'heightMetres': self.height.metres,
            'heightFeet': self.height.feet,
        }
