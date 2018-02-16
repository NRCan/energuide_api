import pytest
from energuide import element
from energuide.embedded import heated_floor_area
from energuide.exceptions import InvalidEmbeddedDataTypeException


@pytest.fixture
def sample() -> element.Element:
    doc = """
    <HeatedFloorArea aboveGrade="92.9" belowGrade="185.8" />
    """
    return element.Element.from_string(doc)


BAD_XML_DATA = [
    """
    <HeatedFloorArea aboveGrade="bad" belowGrade="data" />
    """,
    """
    <HeatedFloorArea aboveGrade="92.9" />
    """
]


def test_from_data(sample: element.Element) -> None:
    output = heated_floor_area.HeatedFloorArea.from_data(sample)
    assert output.area_above_grade.square_metres == 92.9
    assert output.area_below_grade.square_feet == 1999.93468342048


@pytest.mark.parametrize("bad_xml", BAD_XML_DATA)
def test_bad_data(bad_xml: str) -> None:
    floor_area_node = element.Element.from_string(bad_xml)
    with pytest.raises(InvalidEmbeddedDataTypeException) as excinfo:
        heated_floor_area.HeatedFloorArea.from_data(floor_area_node)

    assert excinfo.value.data_class == heated_floor_area.HeatedFloorArea


def test_to_dict(sample: element.Element) -> None:
    output = heated_floor_area.HeatedFloorArea.from_data(sample).to_dict()
    assert output['areaAboveGradeMetres'] == 92.9
    assert output['areaBelowGradeMetres'] == 185.8
