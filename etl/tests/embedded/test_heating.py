import typing
import pytest
from energuide import bilingual
from energuide import element
from energuide.exceptions import InvalidEmbeddedDataTypeError
from energuide.embedded import heating


def sample_node(heating_type: str = 'Furnace',
                equipment_node: typing.Optional[element.Element] = None,
                specification_node: typing.Optional[element.Element] = None) -> element.Element:
    specification_node = sample_specifications() if not specification_node else specification_node
    equipment_node = sample_equipment() if not equipment_node else equipment_node
    heating_node = sample_heating_node(heating_type)

    data = """
<HeatingCooling id="18">
    <Label>Heating/Cooling System</Label>
    <CoolingSeason>
        <Start code="1">January</Start>
        <End code="12">December</End>
        <Design code="7">July</Design>
    </CoolingSeason>
    <Type1>
        <FansAndPump hasEnergyEfficientMotor="false">
            <Mode code="1">
                <English>Auto</English>
                <French>Auto</French>
            </Mode>
            <Power isCalculated="true" low="0" high="145.5" />
        </FansAndPump>
    </Type1>
    <Type2 shadingInF280Cooling="AccountedFor" />
</HeatingCooling>
    """
    node = element.Element.from_string(data)
    type1_node: element.Element = node.xpath('Type1')[0]
    type1_node.insert(1, heating_node)

    heating_node.insert(1, specification_node)
    heating_node.insert(2, equipment_node)
    return node


def sample_heating_node(node_name: str) -> element.Element:
    node = element.Element.new(node_name)

    equip_info_str = """
<EquipmentInformation energystar="false">
    <Manufacturer>Wizard SPH man</Manufacturer>
</EquipmentInformation>
    """
    equip_info_node = element.Element.from_string(equip_info_str)
    node.insert(0, equip_info_node)
    return node


def sample_specifications(efficiency: float = 95.0,
                          is_steady_state: bool = False,
                          capacity: float = 26.5,
                          capacity_units: str = 'kW') -> element.Element:
    data = f"""
<Specifications sizingFactor="1.1" efficiency="{efficiency}" isSteadyState="{'true' if is_steady_state else 'false'}" pilotLight="0" flueDiameter="0">
    <OutputCapacity code="2" value="{capacity}" uiUnits="{capacity_units}" />
</Specifications>
    """
    return element.Element.from_string(data)


def sample_equipment(energy_source_code: int = 2,
                     equipment_type_english: str = 'English Type',
                     equipment_type_french: str = 'French Type') -> element.Element:
    data = f"""
<Equipment isBiEnergy="false" switchoverTemperature="0">
    <EnergySource code="{energy_source_code}" />
    <EquipmentType>
        <English>{equipment_type_english}</English>
        <French>{equipment_type_french}</French>
    </EquipmentType>
</Equipment>
    """
    return element.Element.from_string(data)


@pytest.fixture
def sample_raw() -> element.Element:
    return sample_node()


@pytest.fixture
def sample() -> heating.Heating:
    return heating.Heating(
        heating_type=heating.HeatingType.FURNACE,
        energy_source=heating.EnergySource.NATURAL_GAS,
        equipment_type=bilingual.Bilingual(english='English Type', french='French Type'),
        label='Heating/Cooling System',
        output_size=26.5,
        efficiency=95.0,
        steady_state='AFUE'
    )


def test_from_data(sample_raw: element.Element, sample: heating.Heating) -> None:
    output = heating.Heating.from_data(sample_raw)
    assert output == sample


@pytest.mark.parametrize("unit", ['btu/hr', 'btu/h'])
def test_converts_btu(unit: str) -> None:
    specification_node = sample_specifications(capacity=1000.0, capacity_units=unit)
    node = sample_node(specification_node=specification_node)
    output = heating.Heating.from_data(node)
    assert output.output_size == 0.2930710386613453


def test_output_size_unknown_units() -> None:
    specification_node = sample_specifications(capacity_units='foo')
    node = sample_node(specification_node=specification_node)

    with pytest.raises(InvalidEmbeddedDataTypeError) as ex:
        heating.Heating.from_data(node)
    assert ex.value.data_class == heating.Heating


def test_unknown_heating_type() -> None:
    node = sample_node(heating_type='Foo')

    with pytest.raises(InvalidEmbeddedDataTypeError) as ex:
        heating.Heating.from_data(node)
    assert ex.value.data_class == heating.Heating


def test_boiler() -> None:
    node = sample_node(heating_type='Boiler')
    output = heating.Heating.from_data(node)
    assert output.heating_type == heating.HeatingType.BOILER


@pytest.mark.parametrize("energy_code", [5, 6])
def test_wood_energy_source(energy_code: int) -> None:
    equipment_node = sample_equipment(energy_source_code=energy_code)
    node = sample_node(equipment_node=equipment_node)
    output = heating.Heating.from_data(node)
    assert output.energy_source == heating.EnergySource.WOOD


def test_unknown_energy_source_code() -> None:
    equipment_node = sample_equipment(energy_source_code=9)
    node = sample_node(equipment_node=equipment_node)

    with pytest.raises(InvalidEmbeddedDataTypeError) as ex:
        heating.Heating.from_data(node)
    assert ex.value.data_class == heating.Heating


def test_steady_state() -> None:
    specification_node = sample_specifications(is_steady_state=True)
    node = sample_node(specification_node=specification_node)
    output = heating.Heating.from_data(node)
    assert output.steady_state == 'Steady State'


def test_to_dict(sample: heating.Heating) -> None:
    assert sample.to_dict() == {
        'label': 'Heating/Cooling System',
        'heatingTypeEnglish': 'Furnace',
        'heatingTypeFrench': 'Fournaise',
        'energySourceEnglish': 'Natural Gas',
        'energySourceFrench': 'Chauffage au gaz naturel',
        'equipmentTypeEnglish': 'English Type',
        'equipmentTypeFrench': 'French Type',
        'outputSizeKW': 26.5,
        'outputSizeBtu': 90421.76299999999,
        'efficiency': 95.0,
        'steadyState': 'AFUE',
    }
