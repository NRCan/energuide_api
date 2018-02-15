import typing
from energuide import bilingual
from energuide import element
from energuide.embedded import distance
from energuide.embedded import area
from energuide.embedded import insulation
from energuide.exceptions import InvalidEmbeddedDataTypeException


class _Door(typing.NamedTuple):
    label: str
    door_type: bilingual.Bilingual
    door_insulation: insulation.Insulation
    height: distance.Distance
    width: distance.Distance


class Door(_Door):
    _RSI_MULTIPLIER = 5.678263337

    @classmethod
    def from_data(cls, door: element.Element) -> 'Door':
        try:
            return Door(
                label=door.get_text('Label'),
                door_type=bilingual.Bilingual(
                    english=door.get_text('Construction/Type/English'),
                    french=door.get_text('Construction/Type/French'),
                ),
                door_insulation=insulation.Insulation(float(door.xpath('Construction/Type/@value')[0])),
                height=distance.Distance(float(door.xpath('Measurements/@height')[0])),
                width=distance.Distance(float(door.xpath('Measurements/@width')[0])),
            )
        except (IndexError, ValueError, AssertionError) as e:
            raise InvalidEmbeddedDataTypeException(Door, parent=e)

    @property
    def u_factor(self) -> float:
        return 1 / self.door_insulation.rsi

    @property
    def u_factor_imperial(self) -> float:
        return self.u_factor / self._RSI_MULTIPLIER

    @property
    def _door_area(self) -> area.Area:
        return area.Area(self.height.metres * self.width.metres)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'typeEnglish': self.door_type.english,
            'typeFrench': self.door_type.french,
            'insulationRsi': self.door_insulation.rsi,
            'insulationR': self.door_insulation.r_value,
            'uFactor': self.u_factor,
            'uFactorImperial': self.u_factor_imperial,
            'areaMetres': self._door_area.square_metres,
            'areaFeet': self._door_area.square_feet,
        }
