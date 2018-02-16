import pytest
from energuide import element
from energuide.embedded import heated_floor_area

@pytest.fixture
def sample() -> element.Element:
    doc = """
    <HeatedFloorArea aboveGrade="92.9" belowGrade="185.8" />
    """
    return element.Element.from_string(doc)


def test_from_data(sample: element.Element) -> None:
    output = heated_floor_area.HeatedFloorArea.from_data(sample)
    assert output.area_above_grade.square_metres == 92.9
    assert output.area_below_grade.square_feet == 1999.93468342048


def test_to_dict(sample: element.Element) -> None:
    output = heated_floor_area.HeatedFloorArea.from_data(sample).to_dict()
    assert output['areaAboveGradeMetres'] == 92.9
    assert output['areaBelowGradeMetres'] == 185.8
