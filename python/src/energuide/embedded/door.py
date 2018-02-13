import typing
from energuide import bilingual
from energuide import element


class _Door(typing.NamedTuple):
    label: str
    door_type: bilingual.Bilingual
    rsi: float
    height: float
    width: float


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
            height=float(door.xpath('Measurements/@height')[0]),
            width=float(door.xpath('Measurements/@width')[0]),
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
    def area_metres(self) -> float:
        return self.height * self.width

    @property
    def area_feet(self) -> float:
        return self.area_metres * self._FEET_SQUARED_MULTIPLIER

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'typeEnglish': self.door_type.english,
            'typeFrench': self.door_type.french,
            'rsi': self.rsi,
            'rValue': self.r_value,
            'uFactor': self.u_factor,
            'uFactorImperial': self.u_factor_imperial,
            'areaMetres': self.area_metres,
            'areaFeet': self.area_feet,
        }
