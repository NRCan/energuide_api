import pytest
from energuide.embedded import distance


def test_distance() -> None:
    output = distance.Distance(1)
    assert output.metres == 1.0
    assert output.feet == pytest.approx(3.28084)


def test_from_square_feet() -> None:
    output = distance.Distance.from_feet(1)
    assert output.metres == pytest.approx(0.304800)
    assert output.feet == pytest.approx(1.0)


def test_equality() -> None:
    version1 = distance.Distance(1)
    version2 = distance.Distance(1)

    assert version1 == version2
