import typing
from energuide.embedded import measurement


def test_measurement_to_dict() -> None:
    assert measurement.Measurement(
        measurement=5,
        upgrade=7
    ).to_dict() == {
        'measurement': 5,
        'upgrade': 7,
    }


def test_seriealize_properties() -> None:

    class Test():

        def __init__(self, a: int) -> None:
            self.a = a

        def to_dict(self) -> typing.Dict[str, int]:
            return {
                'a': self.a
            }

    assert measurement.Measurement(
        measurement=Test(1),
        upgrade=Test(2)
    ).to_dict() == {
        'measurement': {
            'a': 1
        },
        'upgrade': {
            'a': 2
        },
    }