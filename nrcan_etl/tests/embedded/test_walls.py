from energuide.embedded import walls
from energuide.embedded import composite


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

