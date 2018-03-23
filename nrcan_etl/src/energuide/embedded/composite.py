import typing

class _CompositeValue(typing.NamedTuple):
    percentage: float
    value: float
    value_name: str

class CompositeValue(_CompositeValue):

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'percentage': self.percentage,
            self.value_name: self.value,
        }
