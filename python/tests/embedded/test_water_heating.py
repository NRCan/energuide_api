import pytest
from energuide import element
from energuide.embedded import water_heating
from energuide.exceptions import InvalidEmbeddedDataTypeException


@pytest.fixture
def sample() -> element.Element:
    data = """
<HotWater>
<Primary hasDrainWaterHeatRecovery="false" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" """ + \
"""energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
    <EquipmentInformation>
        <Manufacturer>Wizard DHW man</Manufacturer>
        <Model>Wizard DHW mod</Model>
    </EquipmentInformation>
    <EnergySource code="1">
        <English>Electricity</English>
        <French>Électricité</French>
    </EnergySource>
    <TankType code="2">
        <English>Conventional tank</English>
        <French>Réservoir classique</French>
    </TankType>
    <TankVolume code="4" value="189.3001">
        <English>189.3 L, 41.6 Imp, 50 US gal</English>
        <French>189.3 L, 41.6 imp, 50 gal ÉU</French>
    </TankVolume>
    <EnergyFactor code="1" value="0.8217" inputCapacity="0">
        <English>Use defaults</English>
        <French>Valeurs par défaut</French>
    </EnergyFactor>
    <TankLocation code="2">
        <English>Basement</English>
        <French>Sous-sol</French>
    </TankLocation>
</Primary>
</HotWater>
    """
    return element.Element.from_string(data)


BAD_XML_DATA = [
    """
<HotWater>
    <Primary hasDrainWaterHeatRecovery="true" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" """ + \
    """energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
        <EquipmentInformation>
            <Manufacturer>Wizard DHW man</Manufacturer>
            <Model>Wizard DHW mod</Model>
        </EquipmentInformation>
        <EnergySource code="1">
            <English>Electricity</English>
            <French>Électricité</French>
        </EnergySource>
        <TankType code="2">
            <English>Conventional tank</English>
            <French>Réservoir classique</French>
        </TankType>
        <TankVolume code="4" value="189.3001">
            <English>189.3 L, 41.6 Imp, 50 US gal</English>
            <French>189.3 L, 41.6 imp, 50 gal ÉU</French>
        </TankVolume>
        <EnergyFactor code="1" value="0.8217" inputCapacity="0">
            <English>Use defaults</English>
            <French>Valeurs par défaut</French>
        </EnergyFactor>
        <TankLocation code="2">
            <English>Basement</English>
            <French>Sous-sol</French>
        </TankLocation>
    </Primary>
</HotWater>
    """,
    """
<HotWater>
    <Primary hasDrainWaterHeatRecovery="false" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" """ + \
    """energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
    </Primary>
</HotWater>
    """,
    """
<HotWater>
    <Primary hasDrainWaterHeatRecovery="false" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" """ + \
    """energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
        <EquipmentInformation>
            <Manufacturer>Wizard DHW man</Manufacturer>
            <Model>Wizard DHW mod</Model>
        </EquipmentInformation>
        <EnergySource code="1">
            <English>Something That Doesn't Exist</English>
            <French>Électricité</French>
        </EnergySource>
        <TankType code="2">
            <English>Something That Doesn't Exist tank</English>
            <French>Réservoir classique</French>
        </TankType>
        <TankVolume code="4" value="189.3001">
            <English>189.3 L, 41.6 Imp, 50 US gal</English>
            <French>189.3 L, 41.6 imp, 50 gal ÉU</French>
        </TankVolume>
        <EnergyFactor code="1" value="0.8217" inputCapacity="0">
            <English>Use defaults</English>
            <French>Valeurs par défaut</French>
        </EnergyFactor>
        <TankLocation code="2">
            <English>Basement</English>
            <French>Sous-sol</French>
        </TankLocation>
    </Primary>
</HotWater>
    """,
    """
<HotWater>
    <Primary hasDrainWaterHeatRecovery="false" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" """ + \
    """energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
        <EquipmentInformation>
            <Manufacturer>Wizard DHW man</Manufacturer>
            <Model>Wizard DHW mod</Model>
        </EquipmentInformation>
        <EnergySource code="1">
            <English>Electricity</English>
            <French>Électricité</French>
        </EnergySource>
        <TankType code="2">
            <English>Conventional tank</English>
            <French>Réservoir classique</French>
        </TankType>
        <TankVolume code="4">
            <English>189.3 L, 41.6 Imp, 50 US gal</English>
            <French>189.3 L, 41.6 imp, 50 gal ÉU</French>
        </TankVolume>
        <EnergyFactor>
            <English>Use defaults</English>
            <French>Valeurs par défaut</French>
        </EnergyFactor>
        <TankLocation code="2">
            <English>Basement</English>
            <French>Sous-sol</French>
        </TankLocation>
    </Primary>
</HotWater>
    """,
    """
<HotWater>
    <Primary hasDrainWaterHeatRecovery="false" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" """ + \
    """energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
        <EquipmentInformation>
            <Manufacturer>Wizard DHW man</Manufacturer>
            <Model>Wizard DHW mod</Model>
        </EquipmentInformation>
        <EnergySource code="1">
            <English>Electricity</English>
            <French>Électricité</French>
        </EnergySource>
        <TankType code="2">
            <English>Conventional tank</English>
            <French>Réservoir classique</French>
        </TankType>
        <TankVolume code="4" value="bad">
            <English>189.3 L, 41.6 Imp, 50 US gal</English>
            <French>189.3 L, 41.6 imp, 50 gal ÉU</French>
        </TankVolume>
        <EnergyFactor code="1" value="data" inputCapacity="0">
            <English>Use defaults</English>
            <French>Valeurs par défaut</French>
        </EnergyFactor>
        <TankLocation code="2">
            <English>Basement</English>
            <French>Sous-sol</French>
        </TankLocation>
    </Primary>
</HotWater>
    """
]


def test_from_data(sample: element.Element) -> None:
    output = water_heating.WaterHeating.from_data(sample)[0]
    assert output.water_heater_type == water_heating.WaterHeaterType.ELECTRICITY_CONVENTIONAL_TANK
    assert output.efficiency == 0.8217


@pytest.mark.parametrize("bad_xml", BAD_XML_DATA)
def test_bad_data(bad_xml: str) -> None:
    water_heating_node = element.Element.from_string(bad_xml)
    with pytest.raises(InvalidEmbeddedDataTypeException) as excinfo:
        water_heating.WaterHeating.from_data(water_heating_node)

    assert excinfo.value.data_class == water_heating.WaterHeating


def test_to_dict(sample: element.Element) -> None:
    output = water_heating.WaterHeating.from_data(sample)[0].to_dict()
    assert output == {
        'typeEnglish': 'Electric storage tank',
        'typeFrench': 'Réservoir électrique',
        'tankVolumeLitres': 189.3001,
        'TankVolumeGallon': 50.0077860172,
        'efficiency': 0.8217,
    }


def test_properties(sample: element.Element) -> None:
    output = water_heating.WaterHeating.from_data(sample)[0]
    assert output.tank_volume_gallon == 50.0077860172
