import enum
import typing
from energuide import bilingual
from energuide import element
from energuide.exceptions import InvalidEmbeddedDataTypeError, ElementGetValueError


class WaterHeaterType(enum.Enum):
    NOT_APPLICABLE = enum.auto()
    DRAIN_WATER_HEAT_RECOVERY = enum.auto()
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
    tank_volume: typing.Optional[float]
    efficiency_ef: typing.Optional[float]
    efficiency_percentage: typing.Optional[float]
    drain_water_heat_recovery_efficiency_percentage: typing.Optional[float]


class WaterHeating(_WaterHeating):

    _LITRE_TO_GALLON = 0.264172

    _TYPE_MAP = {
        ("not applicable", "not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("electricity", "not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("electricity", "conventional tank"): WaterHeaterType.ELECTRICITY_CONVENTIONAL_TANK,
        ("electricity", "conserver tank"): WaterHeaterType.ELECTRICITY_CONSERVER_TANK,
        ("electricity", "instantaneous"): WaterHeaterType.ELECTRICITY_INSTANTANEOUS,
        ("electricity", "tankless heat pump"): WaterHeaterType.ELECTRICITY_TANKLESS_HEAT_PUMP,
        ("electricity", "heat pump"): WaterHeaterType.ELECTRICITY_HEAT_PUMP,
        ("electricity", "add-on heat pump"): WaterHeaterType.ELECTRICITY_ADDON_HEAT_PUMP,
        ("electricity", "integrated heat pump"): WaterHeaterType.ELECTRICITY_ADDON_HEAT_PUMP,
        ("natural gas", "not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("natural gas", "conventional tank"): WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK,
        ("natural gas", "conventional tank (pilot)"): WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK_PILOT,
        ("natural gas", "tankless coil"): WaterHeaterType.NATURAL_GAS_TANKLESS_COIL,
        ("natural gas", "instantaneous"): WaterHeaterType.NATURAL_GAS_INSTANTANEOUS,
        ("natural gas", "instantaneous (condensing)"): WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_CONDENSING,
        ("natural gas", "instantaneous (pilot)"): WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_PILOT,
        ("natural gas", "induced draft fan"): WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN,
        ("natural gas", "induced draft fan (pilot)"): WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN_PILOT,
        ("natural gas", "direct vent (sealed)"): WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED,
        ("natural gas", "direct vent (sealed, pilot)"): WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED_PILOT,
        ("natural gas", "condensing"): WaterHeaterType.NATURAL_GAS_CONDENSING,
        ("oil", "not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("oil", "conventional tank"): WaterHeaterType.OIL_CONVENTIONAL_TANK,
        ("oil", "tankless coil"): WaterHeaterType.OIL_TANKLESS_COIL,
        ("propane", "not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("propane", "conventional tank"): WaterHeaterType.PROPANE_CONVENTIONAL_TANK,
        ("propane", "conventional tank (pilot)"): WaterHeaterType.PROPANE_CONVENTIONAL_TANK_PILOT,
        ("propane", "tankless coil"): WaterHeaterType.PROPANE_TANKLESS_COIL,
        ("propane", "instantaneous"): WaterHeaterType.PROPANE_INSTANTANEOUS,
        ("propane", "instantaneous (condensing)"): WaterHeaterType.PROPANE_INSTANTANEOUS_CONDENSING,
        ("propane", "instantaneous (pilot)"): WaterHeaterType.PROPANE_INSTANTANEOUS_PILOT,
        ("propane", "induced draft fan"): WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN,
        ("propane", "induced draft fan (pilot)"): WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN_PILOT,
        ("propane", "direct vent (sealed)"): WaterHeaterType.PROPANE_DIRECT_VENT_SEALED,
        ("propane", "direct vent (sealed, pilot)"): WaterHeaterType.PROPANE_DIRECT_VENT_SEALED_PILOT,
        ("propane", "condensing"): WaterHeaterType.PROPANE_CONDENSING,
        ("mixed wood", "not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("mixed wood", "fireplace"): WaterHeaterType.WOOD_SPACE_HEATING_FIREPLACE,
        ("mixed wood", "wood stove water coil"): WaterHeaterType.WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL,
        ("mixed wood", "indoor wood boiler"): WaterHeaterType.WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER,
        ("mixed wood", "outdoor wood boiler"): WaterHeaterType.WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER,
        ("mixed wood", "wood hot water tank"): WaterHeaterType.WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK,
        ("hardwood", "not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("hardwood", "fireplace"): WaterHeaterType.WOOD_SPACE_HEATING_FIREPLACE,
        ("hardwood", "wood stove water coil"): WaterHeaterType.WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL,
        ("hardwood", "indoor wood boiler"): WaterHeaterType.WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER,
        ("hardwood", "outdoor wood boiler"): WaterHeaterType.WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER,
        ("hardwood", "wood hot water tank"): WaterHeaterType.WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK,
        ("soft wood", "not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("soft wood", "fireplace"): WaterHeaterType.WOOD_SPACE_HEATING_FIREPLACE,
        ("soft wood", "wood stove water coil"): WaterHeaterType.WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL,
        ("soft wood", "indoor wood boiler"): WaterHeaterType.WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER,
        ("soft wood", "outdoor wood boiler"): WaterHeaterType.WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER,
        ("soft wood", "wood hot water tank"): WaterHeaterType.WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK,
        ("wood pellets", "not applicable"): WaterHeaterType.NOT_APPLICABLE,
        ("wood pellets", "fireplace"): WaterHeaterType.WOOD_SPACE_HEATING_FIREPLACE,
        ("wood pellets", "wood stove water coil"): WaterHeaterType.WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL,
        ("wood pellets", "indoor wood boiler"): WaterHeaterType.WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER,
        ("wood pellets", "outdoor wood boiler"): WaterHeaterType.WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER,
        ("wood pellets", "wood hot water tank"): WaterHeaterType.WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK,
        ("solar", "solar collector system"): WaterHeaterType.SOLAR_COLLECTOR_SYSTEM,
        ("csa p9-11 tested combo heat/dhw", "csa p9-11 tested combo heat/dhw"): WaterHeaterType.CSA_DHW,
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
    def _get_drain_water_heat_recovery(cls, drain_heat_node: element.Element) -> 'WaterHeating':
        efficiency = drain_heat_node.get('@effectivenessAt9.5', float)

        return WaterHeating(
            water_heater_type=WaterHeaterType.DRAIN_WATER_HEAT_RECOVERY,
            tank_volume=None,
            efficiency_ef=None,
            efficiency_percentage=efficiency,
        )

    @classmethod
    def _from_data(cls, water_heating: element.Element) -> 'WaterHeating':
        drain_water_efficiency: type.Optional[float] = None
        if water_heating.get('@hasDrainWaterHeatRecovery', str) == 'true':
            drain_water_efficiency = water_heating.get('DrainWaterHeatRecovery/@effectivenessAt9.5', float)

        try:
            energy_type = water_heating.get_text('EnergySource/English')
            tank_type = water_heating.get_text('TankType/English')

            water_heater_type = cls._TYPE_MAP[(energy_type.lower(), tank_type.lower())]
            volume = water_heating.get('TankVolume/@value', float)
        except ElementGetValueError as exc:
            raise InvalidEmbeddedDataTypeError(WaterHeating, 'Missing/invalid attribue or text') from exc
        except KeyError as exc:
            raise InvalidEmbeddedDataTypeError(WaterHeating, 'Invlaid energy and tank type combination') from exc

        efficiency_ef_node = water_heating.xpath('EnergyFactor/@value')
        efficiency_percent_node = water_heating.xpath('EnergyFactor/@thermalEfficiency')

        if not efficiency_ef_node and not efficiency_percent_node:
            raise InvalidEmbeddedDataTypeError(WaterHeating, 'No efficiency values')

        return WaterHeating(
            water_heater_type=water_heater_type,
            tank_volume=volume,
            efficiency_ef=float(efficiency_ef_node[0]) if efficiency_ef_node else None,
            efficiency_percentage=float(efficiency_percent_node[0]) if efficiency_percent_node else None,
            drain_water_heat_recovery_efficiency_percentage=drain_water_efficiency,
        )

    @classmethod
    def from_data(cls, water_heating: element.Element) -> typing.List['WaterHeating']:
        water_heatings = water_heating.xpath("*[self::Primary or self::Secondary]")

        return [cls._from_data(heater) for heater in water_heatings]

    @property
    def tank_volume_gallon(self) -> float:
        return self.tank_volume * self._LITRE_TO_GALLON

    def to_dict(self) -> typing.Dict[str, typing.Union[str, float, None]]:
        translation = self._WATER_HEATER_TYPE_TRANSLATION[self.water_heater_type]

        return {
            'typeEnglish': translation.english,
            'typeFrench': translation.french,
            'tankVolumeLitres': self.tank_volume,
            'tankVolumeGallon': self.tank_volume_gallon,
            'efficiencyEf': self.efficiency_ef,
            'efficiencyPercentage': self.efficiency_percentage,
            'drainWaterHeatRecoveryEfficiencyPercentage': self.drain_water_heat_recovery_efficiency_percentage,
        }
