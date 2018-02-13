import typing
from energuide import bilingual
from energuide import element
from energuide.embedded import distance
from energuide.embedded import area

class _Door(typing.NamedTuple):
    label: str
    door_type: bilingual.Bilingual
    rsi: float
    height: distance.Distance
    width: distance.Distance


class Door(_Door):
    _RSI_MULTIPLIER = 5.678263337
    _FEET_MULTIPLIER = 3.28084
    _FEET_SQUARED_MULTIPLIER = _FEET_MULTIPLIER ** 2

    @classmethod
    def from_data(cls, door: element.Element) -> 'Door':
        return Door(
            label=door.get_text('Label'),
            door_type=bilingual.Bilingual(
                english=door.get_text('Construction/Type/English'),
                french=door.get_text('Construction/Type/French'),
            ),
            rsi=float(door.xpath('Construction/Type/@value')[0]),
            height=distance.Distance(float(door.xpath('Measurements/@height')[0])),
            width=distance.Distance(float(door.xpath('Measurements/@width')[0])),
        )

    @property
    def r_value(self) -> float:
        return self.rsi * self._RSI_MULTIPLIER

    @property
    def u_factor(self) -> float:
        return 1 / self.rsi

    @property
    def u_factor_imperial(self) -> float:
        return self.u_factor / self._RSI_MULTIPLIER

    @property
    def _door_area(self) -> area.Area:
        return area.Area(self.height.metres * self.width.metres)

    #@property
    #def area_feet(self) -> float:
    #    return self.area_metres * self._FEET_SQUARED_MULTIPLIER

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'typeEnglish': self.door_type.english,
            'typeFrench': self.door_type.french,
            'rsi': self.rsi,
            'rValue': self.r_value,
            'uFactor': self.u_factor,
            'uFactorImperial': self.u_factor_imperial,
            'areaMetres': self._door_area.square_metres,
            'areaFeet': self._door_area.square_feet,
        }
