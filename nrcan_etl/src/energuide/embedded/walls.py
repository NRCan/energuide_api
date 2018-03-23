import itertools
import typing


def from_data(insulation: typing.Optional[str], heat_lost: typing.Optional[float]) -> typing.Dict[str, typing.Any]:
    args = [iter(insulation.split(';'))] * 2
    groups = itertools.zip_longest(fillvalue='0', *args)

    wall_info = {
        'insulation': [
            {
                'percentage': float(percentage),
                'rValue': float(r_value),
            } for percentage, r_value in groups
        ],
        'heatLost': heat_lost
    }

    return wall_info
