import pytest
from energuide.embedded import area


def test_area() -> None:
    output = area.Area(1)
    assert output.square_metres == 1.0
    assert output.square_feet == pytest.approx(10.763911)


def test_from_square_feet() -> None:
    output = area.Area.from_square_feet(1)
    assert output.square_metres == pytest.approx(0.092903)
    assert output.square_feet == pytest.approx(1.0)


def test_equality() -> None:
    version1 = area.Area(1)
    version2 = area.Area(1)

    assert version1 == version2
