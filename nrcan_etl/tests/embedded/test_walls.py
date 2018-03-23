from energuide.embedded import walls

def test_from_data() -> None:
    insulation = '50;2;50;5'
    heat_lost = 10

    assert walls.from_data(insulation, heat_lost) == {
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