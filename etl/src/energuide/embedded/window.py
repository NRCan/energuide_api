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
                window_insulation=insulation.Insulation(float(window.xpath('Construction/Type/@rValue')[0])),
                width=distance.Distance(float(window.xpath('Measurements/@width')[0]) / _MILLIMETRES_TO_METRES),
                height=distance.Distance(float(window.xpath('Measurements/@height')[0]) / _MILLIMETRES_TO_METRES),
            )
        except (ElementGetValueError, ValueError, IndexError) as exc:
            raise InvalidEmbeddedDataTypeError(Window) from exc

    @property
    def _window_area(self) -> area.Area:
        return area.Area(self.width.metres * self.height.metres)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'insulationRsi': self.window_insulation.rsi,
            'insulationR': self.window_insulation.r_value,
            'glazingTypesEnglish': self.window_code.glazing_type.english if self.window_code else None,
            'glazingTypesFrench': self.window_code.glazing_type.french if self.window_code else None,
            'coatingsTintsEnglish': self.window_code.coating_tint.english if self.window_code else None,
            'coatingsTintsFrench': self.window_code.coating_tint.french if self.window_code else None,
            'fillTypeEnglish': self.window_code.fill_type.english if self.window_code else None,
            'fillTypeFrench': self.window_code.fill_type.french if self.window_code else None,
            'spacerTypeEnglish': self.window_code.spacer_type.english if self.window_code else None,
            'spacerTypeFrench': self.window_code.spacer_type.french if self.window_code else None,
            'typeEnglish': self.window_code.window_code_type.english if self.window_code else None,
            'typeFrench': self.window_code.window_code_type.french if self.window_code else None,
            'frameMaterialEnglish': self.window_code.frame_material.english if self.window_code else None,
            'frameMaterialFrench': self.window_code.frame_material.french if self.window_code else None,
            'areaMetres': self._window_area.square_metres,
            'areaFeet': self._window_area.square_feet,
            'widthMetres': self.width.metres,
            'widthFeet': self.width.feet,
            'heightMetres': self.height.metres,
            'heightFeet': self.height.feet,
        }
