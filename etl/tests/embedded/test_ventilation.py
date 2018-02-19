import pytest
from energuide import element
from energuide.embedded import ventilation
from energuide.exceptions import InvalidEmbeddedDataTypeError


@pytest.fixture
def sample() -> element.Element:
    data = """
<Hrv supplyFlowrate="220" exhaustFlowrate="220" fanPower1="509.14" isDefaultFanpower="true" """ + \
"""isEnergyStar="false" isHomeVentilatingInstituteCertified="false" isSupplemental="false" """ + \
"""temperatureCondition1="0" temperatureCondition2="-25" fanPower2="624.08" efficiency1="55" efficiency2="45" """ + \
"""preheaterCapacity="0" lowTempVentReduction="0" coolingEfficiency="25">
    <EquipmentInformation />
    <VentilatorType code="1">
        <English>HRV</English>
        <French>VRC</French>
    </VentilatorType>
</Hrv>
    """
    return element.Element.from_string(data)

BAD_XML_DATA = [
    # This XML block has non-numberic strings for all attribute values
    """
<Hrv supplyFlowrate="words" exhaustFlowrate="words" fanPower1="words" isDefaultFanpower="words" """ + \
"""isEnergyStar="words" isHomeVentilatingInstituteCertified="words" isSupplemental="words" """ + \
"""temperatureCondition2="words" fanPower2="words" efficiency1="words" efficiency2="words" """ + \
"""preheaterCapacity="words" temperatureCondition1="words" lowTempVentReduction="words" coolingEfficiency="words">
    <EquipmentInformation />
    <VentilatorType code="1">
        <English>HRV</English>
        <French>VRC</French>
    </VentilatorType>
</Hrv>
    """,

    # This XML block is missing all attribute values of the <Hrv> tag
    """
<Hrv>
    <EquipmentInformation />
    <VentilatorType code="1">
        <English>HRV</English>
        <French>VRC</French>
    </VentilatorType>
</Hrv>
    """
]

def test_from_data(sample: element.Element):
    output = ventilation.Ventilation.from_data(sample)
    assert output.ventilation_type == ventilation.VentilationType.NOT_ENERGY_STAR_NOT_INSTITUTE_CERTIFIED
    assert output.air_flow_rate == 220


@pytest.mark.parametrize("bad_xml", BAD_XML_DATA)
def test_bad_data(bad_xml: str) -> None:
    ventilation_node = element.Element.from_string(bad_xml)
    with pytest.raises(InvalidEmbeddedDataTypeError) as excinfo:
        ventilation.Ventilation.from_data(ventilation_node)

    assert excinfo.value.data_class == ventilation.Ventilation


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
