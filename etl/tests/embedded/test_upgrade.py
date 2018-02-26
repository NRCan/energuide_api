import pytest
from energuide import element
from energuide.embedded import upgrade


@pytest.fixture
def sample_raw() -> element.Element:
    doc = """
        <CathedralCeilingsFlat cost="0" priority="1" />
    """
    return element.Element.from_string(doc)


@pytest.fixture
def sample() -> upgrade.Upgrade:
    return upgrade.Upgrade(
        upgrade_type='CathedralCeilingsFlat',
        cost=0,
        priority=1,
    )


def test_from_data(sample_raw: element.Element, sample: upgrade.Upgrade) -> None:
    output = upgrade.Upgrade.from_data(sample_raw)
    assert output == sample


def test_to_dict(sample: upgrade.Upgrade) -> None:
    output = sample.to_dict()
    assert output == {
        'upgradeType': 'CathedralCeilingsFlat',
        'cost': 0,
        'priority': 1,
    }
