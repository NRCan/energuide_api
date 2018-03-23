import typing

T = typing.TypeVar('T')
class _Measurement(typing.NamedTuple):
    measurement: T
    upgrade: T

class Measurement(_Measurement):

    def to_dict(self) -> typing.Dict[str, T]:
        return {
            'measurement': self.measurement,
            'upgrade': self.upgrade
        }