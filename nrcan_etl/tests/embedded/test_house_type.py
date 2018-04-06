import typing
import pytest
from energuide.embedded import house_type


def house_types() -> typing.List[typing.Tuple[str, str]]:
    return [
        ("Single detached", "Single detached"),
        ("Detached Duplex", 'Detached duplex'),
        ("Single Detached", 'Single detached'),
        ("Row, end unit", 'Row end unit'),
        ("Row house, end unit", 'Row house end unit'),
        ("Row house, middle unit", 'Row house middle unit'),
        ("Double/Semi-detached", 'Double/semi detached'),
        ("Mobile home", 'Mobile home'),
        ("Apartment Row", 'Apartment row'),
        ("Apartment", 'Apartment'),
        ("Attached Triplex", 'Attached triplex'),
        ("Detached Triplex", 'Detached triplex'),
        ("Attached Duplex", 'Attached duplex'),
        ("Mobile Home", 'Mobile home'),
        ("Double/Semi Detached", 'Double/semi detached'),
        ("Triplex (non-MURB)", 'Triplex non murb'),
        ("Duplex (non-MURB)", 'Duplex non murb'),
        ("Row, middle unit", 'Row middle unit'),
        ("Double/Semi-Detached", 'Double/semi detached'),
        ("Apartment (non-MURB)", 'Apartment non murb'),
    ]


@pytest.mark.parametrize("dirty, clean", house_types())
def test_normalize(dirty, clean):

    assert house_type.HouseType.normalize(dirty) == clean

