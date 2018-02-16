import pytest
from energuide import element
from energuide import extracted_datatypes

# pylint: disable=no-self-use


class TestHeatedFloorArea:

    @pytest.fixture
    def sample(self) -> element.Element:
        doc = """
        <HeatedFloorArea aboveGrade="92.9" belowGrade="185.8" />
        """
        return element.Element.from_string(doc)

    def test_from_data(self, sample: element.Element) -> None:
        output = extracted_datatypes.HeatedFloorArea.from_data(sample)
        assert output.area_above_grade == 92.9
        assert output.area_below_grade_feet == 1999.93468342048

    def test_to_dict(self, sample: element.Element) -> None:
        output = extracted_datatypes.HeatedFloorArea.from_data(sample).to_dict()
        assert output['areaAboveGradeMetres'] == 92.9
        assert output['areaBelowGradeMetres'] == 185.8

    def test_properties(self, sample: element.Element) -> None:
        output = extracted_datatypes.HeatedFloorArea.from_data(sample)
        assert output.area_above_grade_feet == 999.96734171024
        assert output.area_below_grade_feet == 1999.93468342048
