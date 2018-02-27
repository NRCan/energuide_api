import typing
from energuide import element
from energuide.embedded import area
from energuide.embedded import distance
from energuide.embedded import insulation
from energuide.exceptions import InvalidEmbeddedDataTypeError, ElementGetValueError


class _Floor(typing.NamedTuple):
    label: str
    nominal_insulation: insulation.Insulation
    effective_insulation: insulation.Insulation
    floor_area: area.Area
    floor_length: distance.Distance


class Floor(_Floor):

    @classmethod
    def from_data(cls, floor: element.Element) -> 'Floor':
        try:
            return Floor(
                label=floor.get_text('Label'),
                nominal_insulation=insulation.Insulation(floor.get('Construction/Type/@nominalInsulation', float)),
                effective_insulation=insulation.Insulation(floor.get('Construction/Type/@rValue', float)),
                floor_area=area.Area(floor.get('Measurements/@area', float)),
                floor_length=distance.Distance(floor.get('Measurements/@length', float)),
            )
        except (ElementGetValueError) as exc:
            raise InvalidEmbeddedDataTypeError(Floor) from exc

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'insulationNominalRsi': self.nominal_insulation.rsi,
            'insulationNominalR': self.nominal_insulation.r_value,
            'insulationEffectiveRsi': self.effective_insulation.rsi,
            'insulationEffectiveR': self.effective_insulation.r_value,
            'areaMetres': self.floor_area.square_metres,
            'areaFeet': self.floor_area.square_feet,
            'lengthMetres': self.floor_length.metres,
            'lengthFeet': self.floor_length.feet,
        }
