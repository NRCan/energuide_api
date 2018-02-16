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


class TestVentilation:

    @pytest.fixture
    def sample(self) -> element.Element:
        data = """
<Hrv supplyFlowrate="220" exhaustFlowrate="220" fanPower1="509.14" isDefaultFanpower="true" isEnergyStar="false" isHomeVentilatingInstituteCertified="false" isSupplemental="false" temperatureCondition1="0" temperatureCondition2="-25" fanPower2="624.08" efficiency1="55" efficiency2="45" preheaterCapacity="0" lowTempVentReduction="0" coolingEfficiency="25">
    <EquipmentInformation />
    <VentilatorType code="1">
        <English>HRV</English>
        <French>VRC</French>
    </VentilatorType>
</Hrv>
        """
        return element.Element.from_string(data)

    def test_from_data(self, sample: element.Element):
        output = extracted_datatypes.Ventilation.from_data(sample)
        assert output.ventilation_type == extracted_datatypes.VentilationType.NOT_ENERGY_STAR_NOT_INSTITUTE_CERTIFIED
        assert output.air_flow_rate == 220

    def test_to_dict(self, sample: element.Element) -> None:
        output = extracted_datatypes.Ventilation.from_data(sample).to_dict()
        assert output == {
            'typeEnglish': 'Heat recovery ventilator',
            'typeFrench': 'Ventilateur-récupérateur de chaleur',
            'airFlowRateLps': 220,
            'airFlowRateCfm': 466.1536,
            'efficiency': 55,
        }

    def test_properties(self, sample: element.Element) -> None:
        output = extracted_datatypes.Ventilation.from_data(sample)
        assert output.air_flow_rate_cmf == 466.1536


