import typing

T = typing.TypeVar('T')
class _Measurement(typing.NamedTuple):
    measurement: T
    upgrade: T

class Measurement(_Measurement):

    def to_dict(self) -> typing.Dict[str, T]:
        if hasattr(self.measurement, 'to_dict'):
            measurement = self.measurement.to_dict()
        else:
            measurement = self.measurement

        if hasattr(self.upgrade, 'to_dict'):
            upgrade = self.upgrade.to_dict()
        else:
            upgrade = self.upgrade

        return {
            'measurement': measurement,
            'upgrade': measurement,
        }
