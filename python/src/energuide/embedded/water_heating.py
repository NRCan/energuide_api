import enum
import typing
from energuide import bilingual
from energuide import element


_LITRE_TO_GALLON = 0.264172


class WaterHeaterType(enum.Enum):
    NOT_APPLICABLE = enum.auto()
    ELECTRICITY_CONVENTIONAL_TANK = enum.auto()
    ELECTRICITY_CONSERVER_TANK = enum.auto()
    ELECTRICITY_INSTANTANEOUS = enum.auto()
    ELECTRICITY_TANKLESS_HEAT_PUMP = enum.auto()
    ELECTRICITY_HEAT_PUMP = enum.auto()
    ELECTRICITY_ADDON_HEAT_PUMP = enum.auto()
    NATURAL_GAS_CONVENTIONAL_TANK = enum.auto()
    NATURAL_GAS_CONVENTIONAL_TANK_PILOT = enum.auto()
    NATURAL_GAS_TANKLESS_COIL = enum.auto()
    NATURAL_GAS_INSTANTANEOUS = enum.auto()
    NATURAL_GAS_INSTANTANEOUS_CONDENSING = enum.auto()
    NATURAL_GAS_INSTANTANEOUS_PILOT = enum.auto()
    NATURAL_GAS_INDUCED_DRAFT_FAN = enum.auto()
    NATURAL_GAS_INDUCED_DRAFT_FAN_PILOT = enum.auto()
    NATURAL_GAS_DIRECT_VENT_SEALED = enum.auto()
    NATURAL_GAS_DIRECT_VENT_SEALED_PILOT = enum.auto()
    NATURAL_GAS_CONDENSING = enum.auto()
    OIL_CONVENTIONAL_TANK = enum.auto()
    OIL_TANKLESS_COIL = enum.auto()
    PROPANE_CONVENTIONAL_TANK = enum.auto()
    PROPANE_CONVENTIONAL_TANK_PILOT = enum.auto()
    PROPANE_TANKLESS_COIL = enum.auto()
    PROPANE_INSTANTANEOUS = enum.auto()
    PROPANE_INSTANTANEOUS_CONDENSING = enum.auto()
    PROPANE_INSTANTANEOUS_PILOT = enum.auto()
    PROPANE_INDUCED_DRAFT_FAN = enum.auto()
    PROPANE_INDUCED_DRAFT_FAN_PILOT = enum.auto()
    PROPANE_DIRECT_VENT_SEALED = enum.auto()
    PROPANE_DIRECT_VENT_SEALED_PILOT = enum.auto()
    PROPANE_CONDENSING = enum.auto()
    WOOD_SPACE_HEATING_FIREPLACE = enum.auto()
    WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL = enum.auto()
    WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER = enum.auto()
    WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER = enum.auto()
    WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK = enum.auto()
    SOLAR_COLLECTOR_SYSTEM = enum.auto()
    CSA_DHW = enum.auto()


class _WaterHeating(typing.NamedTuple):
    water_heater_type: WaterHeaterType
    tank_volume: float
    efficiency: float


class WaterHeating(_WaterHeating):

    _TYPE_MAP = {
        ("Electricity", "Not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("Electricity", "Conventional tank"): WaterHeaterType.ELECTRICITY_CONVENTIONAL_TANK,
        ("Electricity", "Conserver tank"): WaterHeaterType.ELECTRICITY_CONSERVER_TANK,
        ("Electricity", "Instantaneous"): WaterHeaterType.ELECTRICITY_INSTANTANEOUS,
        ("Electricity", "Tankless heat pump"): WaterHeaterType.ELECTRICITY_TANKLESS_HEAT_PUMP,
        ("Electricity", "Heat pump"): WaterHeaterType.ELECTRICITY_HEAT_PUMP,
        ("Electricity", "Add-on heat pump"): WaterHeaterType.ELECTRICITY_ADDON_HEAT_PUMP,
        ("Natural gas", "Not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("Natural gas", "Conventional tank"): WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK,
        ("Natural gas", "Conventional tank (pilot)"): WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK_PILOT,
        ("Natural gas", "Tankless coil"): WaterHeaterType.NATURAL_GAS_TANKLESS_COIL,
        ("Natural gas", "Instantaneous"): WaterHeaterType.NATURAL_GAS_INSTANTANEOUS,
        ("Natural gas", "Instantaneous (condensing)"): WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_CONDENSING,
        ("Natural gas", "Instantaneous (pilot)"): WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_PILOT,
        ("Natural gas", "Induced draft fan"): WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN,
        ("Natural gas", "Induced draft fan (pilot)"): WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN_PILOT,
        ("Natural gas", "Direct vent (sealed)"): WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED,
        ("Natural gas", "Direct vent (sealed, pilot)"): WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED_PILOT,
        ("Natural gas", "Condensing"): WaterHeaterType.NATURAL_GAS_CONDENSING,
        ("Oil", "Not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("Oil", "Conventional tank"): WaterHeaterType.OIL_CONVENTIONAL_TANK,
        ("Oil", "Tankless coil"): WaterHeaterType.OIL_TANKLESS_COIL,
        ("Propane", "Not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("Propane", "Conventional tank"): WaterHeaterType.PROPANE_CONVENTIONAL_TANK,
        ("Propane", "Conventional tank (pilot)"): WaterHeaterType.PROPANE_CONVENTIONAL_TANK_PILOT,
        ("Propane", "Tankless coil"): WaterHeaterType.PROPANE_TANKLESS_COIL,
        ("Propane", "Instantaneous"): WaterHeaterType.PROPANE_INSTANTANEOUS,
        ("Propane", "Instantaneous (condensing)"): WaterHeaterType.PROPANE_INSTANTANEOUS_CONDENSING,
        ("Propane", "Instantaneous (pilot)"): WaterHeaterType.PROPANE_INSTANTANEOUS_PILOT,
        ("Propane", "Induced draft fan"): WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN,
        ("Propane", "Induced draft fan (pilot)"): WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN_PILOT,
        ("Propane", "Direct vent (sealed)"): WaterHeaterType.PROPANE_DIRECT_VENT_SEALED,
        ("Propane", "Direct vent (sealed, pilot)"): WaterHeaterType.PROPANE_DIRECT_VENT_SEALED_PILOT,
        ("Propane", "Condensing"): WaterHeaterType.PROPANE_CONDENSING,

        (
            "Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)",
            "Not applicable"
        ): WaterHeaterType.NOT_APPLICABLE,

        (
            "Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)",
            "Fireplace"
        ): WaterHeaterType.WOOD_SPACE_HEATING_FIREPLACE,

        (
            "Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)",
            "Wood stove water coil"
        ): WaterHeaterType.WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL,

        (
            "Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)",
            "Indoor wood boiler"
        ): WaterHeaterType.WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER,

        (
            "Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)",
            "Outdoor wood boiler"
        ): WaterHeaterType.WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER,

        (
            "Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)",
            "Wood hot water tank"
        ): WaterHeaterType.WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK,

        ("Solar", "Solar Collector System"): WaterHeaterType.SOLAR_COLLECTOR_SYSTEM,
        ("CSA P9-11 tested Combo Heat/DHW", "CSA P9-11 tested Combo Heat/DHW"): WaterHeaterType.CSA_DHW,
    }

    _WATER_HEATER_TYPE_TRANSLATION = {
        WaterHeaterType.NOT_APPLICABLE: bilingual.Bilingual(
            english="",
            french="",
        ),
        WaterHeaterType.ELECTRICITY_CONVENTIONAL_TANK: bilingual.Bilingual(
            english="Electric storage tank",
            french="Réservoir électrique",
        ),
        WaterHeaterType.ELECTRICITY_CONSERVER_TANK: bilingual.Bilingual(
            english="Electric storage tank",
            french="Réservoir électrique",
        ),
        WaterHeaterType.ELECTRICITY_INSTANTANEOUS: bilingual.Bilingual(
            english="Electric tankless water heater",
            french="Chauffe-eau électrique sans réservoir",
        ),
        WaterHeaterType.ELECTRICITY_TANKLESS_HEAT_PUMP: bilingual.Bilingual(
            english="Electric tankless heat pump",
            french="Thermopompe électrique sans réservoir",
        ),
        WaterHeaterType.ELECTRICITY_HEAT_PUMP: bilingual.Bilingual(
            english="Electric heat pump",
            french="Thermopompe électrique",
        ),
        WaterHeaterType.ELECTRICITY_ADDON_HEAT_PUMP: bilingual.Bilingual(
            english="Integrated heat pump",
            french="Thermopompe intégrée",
        ),
        WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK: bilingual.Bilingual(
            english="Natural gas storage tank",
            french="Réservoir au gaz naturel",
        ),
        WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK_PILOT: bilingual.Bilingual(
            english="Natural gas storage tank with pilot",
            french="Réservoir au gaz naturel avec veilleuse",
        ),
        WaterHeaterType.NATURAL_GAS_TANKLESS_COIL: bilingual.Bilingual(
            english="Natural gas tankless coil",
            french="Serpentin sans réservoir au gaz naturel",
        ),
        WaterHeaterType.NATURAL_GAS_INSTANTANEOUS: bilingual.Bilingual(
            english="Natural gas tankless",
            french="Chauffe-eau instantané au gaz naturel",
        ),
        WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_CONDENSING: bilingual.Bilingual(
            english="Natural gas tankless",
            french="Chauffe-eau instantané au gaz naturel",
        ),
        WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_PILOT: bilingual.Bilingual(
            english="Natural gas tankless with pilot",
            french="Chauffe-eau instantané au gaz naturel avec veilleuse",
        ),
        WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN: bilingual.Bilingual(
            english="Natural gas power vented storage tank",
            french="Réservoir au gaz naturel à évacuation forcée",
        ),
        WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN_PILOT: bilingual.Bilingual(
            english="Natural gas power vented storage tank with pilot",
            french="Réservoir au gaz naturel à évacuation forcée avec veilleuse",
        ),
        WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED: bilingual.Bilingual(
            english="Natural gas direct vented storage tank",
            french="Réservoir au gaz naturel à évacuation directe",
        ),
        WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED_PILOT: bilingual.Bilingual(
            english="Natural gas direct vented storage tank with pilot",
            french="Réservoir au gaz naturel à évacuation directe avec veilleuse",
        ),
        WaterHeaterType.NATURAL_GAS_CONDENSING: bilingual.Bilingual(
            english="Natural gas condensing storage tank",
            french="Réservoir au gaz naturel à condensation",
        ),
        WaterHeaterType.OIL_CONVENTIONAL_TANK: bilingual.Bilingual(
            english="Oil-fired storage tank",
            french="Réservoir au mazout",
        ),
        WaterHeaterType.OIL_TANKLESS_COIL: bilingual.Bilingual(
            english="Oil-type tankless coil",
            french="Serpentin sans réservoir au mazout",
        ),
        WaterHeaterType.PROPANE_CONVENTIONAL_TANK: bilingual.Bilingual(
            english="Propane storage tank",
            french="Réservoir au propane",
        ),
        WaterHeaterType.PROPANE_CONVENTIONAL_TANK_PILOT: bilingual.Bilingual(
            english="Propane storage tank with pilot",
            french="Réservoir au propane avec veilleuse",
        ),
        WaterHeaterType.PROPANE_TANKLESS_COIL: bilingual.Bilingual(
            english="Propane tankless coil",
            french="Serpentin sans réservoir au propane",
        ),
        WaterHeaterType.PROPANE_INSTANTANEOUS: bilingual.Bilingual(
            english="Propane tankless",
            french="Chauffe-eau instantané au propane",
        ),
        WaterHeaterType.PROPANE_INSTANTANEOUS_CONDENSING: bilingual.Bilingual(
            english="Propane condensing tankless",
            french="Chauffe-eau instantané au propane à condensation",
        ),
        WaterHeaterType.PROPANE_INSTANTANEOUS_PILOT: bilingual.Bilingual(
            english="Propane tankless with pilot",
            french="Chauffe-eau instantané au propane avec veilleuse",
        ),
        WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN: bilingual.Bilingual(
            english="Propane power vented storage tank",
            french="Réservoir au propane à évacuation forcée",
        ),
        WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN_PILOT: bilingual.Bilingual(
            english="Propane power vented storage tank with pilot",
            french="Réservoir au propane à évacuation forcée avec veilleuse",
        ),
        WaterHeaterType.PROPANE_DIRECT_VENT_SEALED: bilingual.Bilingual(
            english="Propane power vented storage tank",
            french="Réservoir au propane à évacuation directe",
        ),
        WaterHeaterType.PROPANE_DIRECT_VENT_SEALED_PILOT: bilingual.Bilingual(
            english="Propane power vented storage tank with pilot",
            french="Réservoir au propane à évacuation directe avec veilleuse",
        ),
        WaterHeaterType.PROPANE_CONDENSING: bilingual.Bilingual(
            english="Propane condensing storage tank",
            french="Réservoir au propane à condensation",
        ),
        WaterHeaterType.WOOD_SPACE_HEATING_FIREPLACE: bilingual.Bilingual(
            english="Fireplace",
            french="Foyer",
        ),
        WaterHeaterType.WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL: bilingual.Bilingual(
            english="Wood stove water coil",
            french="Poêle à bois avec serpentin à l'eau",
        ),
        WaterHeaterType.WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER: bilingual.Bilingual(
            english="Indoor wood boiler",
            french="Chaudière intérieure au bois",
        ),
        WaterHeaterType.WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER: bilingual.Bilingual(
            english="Outdoor wood boiler",
            french="Chaudière extérieure au bois",
        ),
        WaterHeaterType.WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK: bilingual.Bilingual(
            english="Wood-fired water storage tank",
            french="Réservoir à eau chaude au bois",
        ),
        WaterHeaterType.SOLAR_COLLECTOR_SYSTEM: bilingual.Bilingual(
            english="Solar domestic water heater",
            french="Chauffe-eau solaire domestique",
        ),
        WaterHeaterType.CSA_DHW: bilingual.Bilingual(
            english="Certified combo system, space and domestic water heating",
            french="Système combiné certifié pour le chauffage des locaux et de l’eau",
        ),
    }

    @classmethod
    def _from_data(cls, water_heating: element.Element) -> 'WaterHeating':
        assert water_heating.attrib['hasDrainWaterHeatRecovery'] == 'false'

        energy_type = water_heating.get_text('EnergySource/English')
        tank_type = water_heating.get_text('TankType/English')

        water_heater_type = cls._TYPE_MAP[(energy_type, tank_type)]
        volume = float(water_heating.xpath('TankVolume/@value')[0])
        efficiency = float(water_heating.xpath('EnergyFactor/@value')[0])

        return WaterHeating(
            water_heater_type=water_heater_type,
            tank_volume=volume,
            efficiency=efficiency,
        )

    @classmethod
    def from_data(cls, water_heating: element.Element) -> typing.List['WaterHeating']:
        water_heatings = water_heating.xpath("*[self::Primary or self::Secondary]")
        return [cls._from_data(water_heating) for water_heating in water_heatings]


    @property
    def tank_volume_gallon(self) -> float:
        return self.tank_volume * _LITRE_TO_GALLON


    def to_dict(self) -> typing.Dict[str, typing.Union[str, float]]:
        translation = self._WATER_HEATER_TYPE_TRANSLATION[self.water_heater_type]
        return {
            'typeEnglish': translation.english,
            'typeFrench': translation.french,
            'tankVolumeLitres': self.tank_volume,
            'TankVolumeGallon': self.tank_volume_gallon,
            'efficiency': self.efficiency,
        }
