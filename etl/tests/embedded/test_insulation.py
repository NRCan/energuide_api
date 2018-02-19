import pytest
from energuide.embedded import insulation


def test_insulation() -> None:
    output = insulation.Insulation(1)
    assert output.rsi == 1.0
    assert output.r_value == pytest.approx(5.678263)


def test_from_r_value() -> None:
    output = insulation.Insulation.from_r_value(1)
    assert output.rsi == pytest.approx(0.17611018)
    assert output.r_value == pytest.approx(1.0)


def test_equality() -> None:
    version1 = insulation.Insulation(1)
    version2 = insulation.Insulation(1)

    assert version1 == version2
