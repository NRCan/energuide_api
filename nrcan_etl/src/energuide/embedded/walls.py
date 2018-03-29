import itertools
import typing
from energuide.embedded import composite
from energuide.exceptions import InvalidEmbeddedDataTypeError


class _Wall(typing.NamedTuple):
    insulation: typing.List[composite.CompositeValue]
    heat_lost: typing.Optional[float]


class Wall(_Wall):

    @classmethod
    def from_data(cls,
                  insulation: typing.Optional[str],
                  heat_lost: typing.Optional[float]) -> 'Wall':

        if insulation:
            args = [iter(insulation.split(';'))] * 2
            groups = itertools.zip_longest(fillvalue='0', *args)

            try:
                composite_insulation = [
                    composite.CompositeValue(
                        percentage=float(percentage),
                        value=float(r_value),
                        value_name='rValue',
                    ) for percentage, r_value in groups
                ]
            except ValueError as exc:
                raise InvalidEmbeddedDataTypeError(Wall, 'Invalid composite insulation string') from exc

        else:
            composite_insulation = []

        return Wall(
            insulation=composite_insulation,
            heat_lost=heat_lost
        )

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'insulation': [
                insulation.to_dict() for insulation in self.insulation
            ],
            'heatLost': self.heat_lost,
        }
