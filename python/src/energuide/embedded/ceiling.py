import typing
from energuide import bilingual
from energuide import element
from energuide.embedded import area
from energuide.embedded import distance
from energuide.embedded import insulation


class _Ceiling(typing.NamedTuple):
    label: str
    ceiling_type: bilingual.Bilingual
    nominal_insulation: insulation.Insulation
    effective_insulation: insulation.Insulation
    ceiling_area: area.Area
    ceiling_length: distance.Distance


class Ceiling(_Ceiling):

    @classmethod
    def from_data(cls, ceiling: element.Element) -> 'Ceiling':
        return Ceiling(
            label=ceiling.get_text('Label'),
            ceiling_type=bilingual.Bilingual(
                english=ceiling.get_text('Construction/Type/English'),
                french=ceiling.get_text('Construction/Type/French'),
            ),
            nominal_insulation=insulation.Insulation(
                float(ceiling.xpath('Construction/CeilingType/@nominalInsulation')[0])),
            effective_insulation=insulation.Insulation(
                float(ceiling.xpath('Construction/CeilingType/@rValue')[0])),
            ceiling_area=area.Area(float(ceiling.xpath('Measurements/@area')[0])),
            ceiling_length=distance.Distance(float(ceiling.xpath('Measurements/@length')[0])),
        )

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'typeEnglish': self.ceiling_type.english,
            'typeFrench': self.ceiling_type.french,
            'nominalRsi': self.nominal_insulation.rsi,
            'nominalR': self.nominal_insulation.r_value,
            'effectiveRsi': self.effective_insulation.rsi,
            'effectiveR': self.effective_insulation.r_value,
            'areaMetres': self.ceiling_area.square_metres,
            'areaFeet': self.ceiling_area.square_feet,
            'lengthMetres': self.ceiling_length.metres,
            'lengthFeet': self.ceiling_length.feet,
        }
