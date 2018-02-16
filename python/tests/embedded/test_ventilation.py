import pytest
from energuide import element
from energuide.embedded import ventilation


@pytest.fixture
def sample() -> element.Element:
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

def test_from_data(sample: element.Element):
    output = ventilation.Ventilation.from_data(sample)
    assert output.ventilation_type == ventilation.VentilationType.NOT_ENERGY_STAR_NOT_INSTITUTE_CERTIFIED
    assert output.air_flow_rate == 220

def test_to_dict(sample: element.Element) -> None:
    output = ventilation.Ventilation.from_data(sample).to_dict()
    assert output == {
        'typeEnglish': 'Heat recovery ventilator',
        'typeFrench': 'Ventilateur-récupérateur de chaleur',
        'airFlowRateLps': 220,
        'airFlowRateCfm': 466.1536,
        'efficiency': 55,
    }

def test_properties(sample: element.Element) -> None:
    output = ventilation.Ventilation.from_data(sample)
    assert output.air_flow_rate_cmf == 466.1536
