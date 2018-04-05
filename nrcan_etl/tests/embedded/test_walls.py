import pytest

from energuide.embedded import walls
from energuide.embedded import composite
from energuide.exceptions import InvalidEmbeddedDataTypeError


def test_from_data() -> None:
    insulation = '50;2;50;5'
    heat_lost = 10

    wall = walls.Wall.from_data(insulation, heat_lost)
    assert wall == walls.Wall(
        insulation=[
            composite.CompositeValue(
                percentage=50.0,
                value=2.0,
                value_name='rValue'
            ),
            composite.CompositeValue(
                percentage=50.0,
                value=5.0,
                value_name='rValue'
            ),
        ],
        heat_lost=10
    )


def test_to_dict() -> None:
    wall = walls.Wall(
        insulation=[
            composite.CompositeValue(
                percentage=50.0,
                value=2.0,
                value_name='rValue'
            ),
            composite.CompositeValue(
                percentage=50.0,
                value=5.0,
                value_name='rValue'
            ),
        ],
        heat_lost=10
    )

    assert wall.to_dict() == {
        'insulation': [
            {
                'percentage': 50.0,
                'rValue': 2.0,
            }, {
                'percentage': 50.0,
                'rValue': 5.0,
            }
        ],
        'heatLost': 10
    }


def test_wall_missing_accepted() -> None:
    wall = walls.Wall.from_data(None, None)
    assert wall.to_dict() == {
        'insulation': [],
        'heatLost': None,
    }


def test_bad_insulation_string() -> None:
    insulation = '50;2.3;50;5..7'
    heat_lost = 10

    with pytest.raises(InvalidEmbeddedDataTypeError) as excinfo:
        walls.Wall.from_data(insulation, heat_lost)

    assert excinfo.value.data_class == walls.Wall


def test_incomplete_insulation_string() -> None:
    insulation = '50;2.3;50'
    heat_lost = 10

    wall = walls.Wall.from_data(insulation, heat_lost)

    wall.insulation[1].value == 0.0
