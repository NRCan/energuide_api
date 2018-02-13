import enum
import typing
from energuide import element
from energuide import bilingual
from energuide.embedded import code


class WaterHeaterType(enum.Enum):
    NOT_APPLICABLE = ""
    ELECTRICITY_CONVENTIONAL_TANK_ENGLISH = "Electric storage tank"
    ELECTRICITY_CONVENTIONAL_TANK_FRENCH = "Réservoir électrique"
    ELECTRICITY_CONSERVER_TANK_ENGLISH = "Electric storage tank"
    ELECTRICITY_CONSERVER_TANK_FRENCH = "Réservoir électrique"
    ELECTRICITY_INSTANTANEOUS_ENGLISH = "Electric tankless water heater"
    ELECTRICITY_INSTANTANEOUS_FRENCH = "Chauffe-eau électrique sans réservoir"
    ELECTRICITY_TANKLESS_HEAT_PUMP_ENGLISH = "Electric tankless heat pump"
    ELECTRICITY_TANKLESS_HEAT_PUMP_FRENCH = "Thermopompe électrique sans réservoir"
    ELECTRICITY_HEAT_PUMP_ENGLISH = "Electric heat pump"
    ELECTRICITY_HEAT_PUMP_FRENCH = "Thermopompe électrique"
    ELECTRICITY_ADDON_HEAT_PUMP_ENGLISH = "Integrated heat pump"
    ELECTRICITY_ADDON_HEAT_PUMP_FRENCH = "Thermopompe intégrée"
    NATURAL_GAS_CONVENTIONAL_TANK_ENGLISH = "Natural gas storage tank"
    NATURAL_GAS_CONVENTIONAL_TANK_FRENCH = "Réservoir au gaz naturel"
    NATURAL_GAS_CONVENTIONAL_TANK_PILOT_ENGLISH = "Natural gas storage tank with pilot"
    NATURAL_GAS_CONVENTIONAL_TANK_PILOT_FRENCH = "Réservoir au gaz naturel avec veilleuse"
    NATURAL_GAS_TANKLESS_COIL_ENGLISH = "Natural gas tankless coil"
    NATURAL_GAS_TANKLESS_COIL_FRENCH = "Serpentin sans réservoir au gaz naturel"
    NATURAL_GAS_INSTANTANEOUS_ENGLISH = "Natural gas tankless"
    NATURAL_GAS_INSTANTANEOUS_FRENCH = "Chauffe-eau instantané au gaz naturel"
    NATURAL_GAS_INSTANTANEOUS_CONDENSING_ENGLISH = "Natural gas tankless"
    NATURAL_GAS_INSTANTANEOUS_CONDENSING_FRENCH = "Chauffe-eau instantané au gaz naturel"
    NATURAL_GAS_INSTANTANEOUS_PILOT_ENGLISH = "Natural gas tankless with pilot"
    NATURAL_GAS_INSTANTANEOUS_PILOT_FRENCH = "Chauffe-eau instantané au gaz naturel avec veilleuse"
    NATURAL_GAS_INDUCED_DRAFT_FAN_ENGLISH = "Natural gas power vented storage tank"
    NATURAL_GAS_INDUCED_DRAFT_FAN_FRENCH = "Réservoir au gaz naturel à évacuation forcée"
    NATURAL_GAS_INDUCED_DRAFT_FAN_PILOT_ENGLISH = "Natural gas power vented storage tank with pilot"
    NATURAL_GAS_INDUCED_DRAFT_FAN_PILOT_FRENCH = "Réservoir au gaz naturel à évacuation forcée avec veilleuse"
    NATURAL_GAS_DIRECT_VENT_SEALED_ENGLISH = "Natural gas direct vented storage tank"
    NATURAL_GAS_DIRECT_VENT_SEALED_FRENCH = "Réservoir au gaz naturel à évacuation directe"
    NATURAL_GAS_DIRECT_VENT_SEALED_PILOT_ENGLISH = "Natural gas direct vented storage tank with pilot"
    NATURAL_GAS_DIRECT_VENT_SEALED_PILOT_FRENCH = "Réservoir au gaz naturel à évacuation directe avec veilleuse"
    NATURAL_GAS_CONDENSING_ENGLISH = "Natural gas condensing storage tank"
    NATURAL_GAS_CONDENSING_FRENCH = "Réservoir au gaz naturel à condensation"
    OIL_CONVENTIONAL_TANK_ENGLISH = "Oil-fired storage tank"
    OIL_CONVENTIONAL_TANK_FRENCH = "Réservoir au mazout"
    OIL_TANKLESS_COIL_ENGLISH = "Oil-type tankless coil"
    OIL_TANKLESS_COIL_FRENCH = "Serpentin sans réservoir au mazout"
    PROPANE_CONVENTIONAL_TANK_ENGLISH = "Propane storage tank"
    PROPANE_CONVENTIONAL_TANK_FRENCH = "Réservoir au propane"
    PROPANE_CONVENTIONAL_TANK_PILOT_ENGLISH = "Propane storage tank with pilot"
    PROPANE_CONVENTIONAL_TANK_PILOT_FRENCH = "Réservoir au propane avec veilleuse"
    PROPANE_TANKLESS_COIL_ENGLISH = "Propane tankless coil"
    PROPANE_TANKLESS_COIL_FRENCH = "Serpentin sans réservoir au propane"
    PROPANE_INSTANTANEOUS_ENGLISH = "Propane tankless"
    PROPANE_INSTANTANEOUS_FRENCH = "Chauffe-eau instantané au propane"
    PROPANE_INSTANTANEOUS_CONDENSING_ENGLISH = "Propane condensing tankless"
    PROPANE_INSTANTANEOUS_CONDENSING_FRENCH = "Chauffe-eau instantané au propane à condensation"
    PROPANE_INSTANTANEOUS_PILOT_ENGLISH = "Propane tankless with pilot"
    PROPANE_INSTANTANEOUS_PILOT_FRENCH = "Chauffe-eau instantané au propane avec veilleuse"
    PROPANE_INDUCED_DRAFT_FAN_ENGLISH = "Propane power vented storage tank"
    PROPANE_INDUCED_DRAFT_FAN_FRENCH = "Réservoir au propane à évacuation forcée"
    PROPANE_INDUCED_DRAFT_FAN_PILOT_ENGLISH = "Propane power vented storage tank with pilot"
    PROPANE_INDUCED_DRAFT_FAN_PILOT_FRENCH = "Réservoir au propane à évacuation forcée avec veilleuse"
    PROPANE_DIRECT_VENT_SEALED_ENGLISH = "Propane power vented storage tank"
    PROPANE_DIRECT_VENT_SEALED_FRENCH = "Réservoir au propane à évacuation directe"
    PROPANE_DIRECT_VENT_SEALED_PILOT_ENGLISH = "Propane power vented storage tank with pilot"
    PROPANE_DIRECT_VENT_SEALED_PILOT_FRENCH = "Réservoir au propane à évacuation directe avec veilleuse"
    PROPANE_CONDENSING_ENGLISH = "Propane condensing storage tank"
    PROPANE_CONDENSING_FRENCH = "Réservoir au propane à condensation"
    WOOD_SPACE_HEATING_FIREPLACE_ENGLISH = "Fireplace"
    WOOD_SPACE_HEATING_FIREPLACE_FRENCH = "Foyer"
    WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL_ENGLISH = "Wood stove water coil"
    WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL_FRENCH = "Poêle à bois avec serpentin à l'eau"
    WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER_ENGLISH = "Indoor wood boiler"
    WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER_FRENCH = "Chaudière intérieure au bois"
    WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER_ENGLISH = "Outdoor wood boiler"
    WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER_FRENCH = "Chaudière extérieure au bois"
    WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK_ENGLISH = "Wood-fired water storage tank"
    WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK_FRENCH = "Réservoir à eau chaude au bois"
    SOLAR_COLLECTOR_SYSTEM_ENGLISH = "Solar domestic water heater"
    SOLAR_COLLECTOR_SYSTEM_FRENCH = "Chauffe-eau solaire domestique"
    CSA_DHW_ENGLISH = "Certified combo system, space and domestic water heating"
    CSA_DHW_FRENCH = "Système combiné certifié pour le chauffage des locaux et de l’eau"


class _Window(typing.NamedTuple):
    label: str
    glazing_type_english: typing.Optional[str]
    glazing_type_french: typing.Optional[str]
    coating_tint_english: typing.Optional[str]
    coating_tint_french: typing.Optional[str]
    fill_type_english: typing.Optional[str]
    fill_type_french: typing.Optional[str]
    spacer_type_english: typing.Optional[str]
    spacer_type_french: typing.Optional[str]
    window_code_type_english: typing.Optional[str]
    window_code_type_french: typing.Optional[str]
    frame_material_english: typing.Optional[str]
    frame_material_french: typing.Optional[str]
    rsi: float
    width: float
    height: float


class _HeatedFloorArea(typing.NamedTuple):
    area_above_grade: typing.Optional[float]
    area_below_grade: typing.Optional[float]


class VentilationType(enum.Enum):
    NOT_APPLICABLE = enum.auto()
    ENERGY_STAR_INSTITUTE_CERTIFIED = enum.auto()
    ENERGY_STAR_NOT_INSTITUTE_CERTIFIED = enum.auto()
    NOT_ENERGY_STAR_INSTITUTE_CERTIFIED = enum.auto()
    NOT_ENERGY_STAR_NOT_INSTITUTE_CERTIFIED = enum.auto()


class _Ventilation(typing.NamedTuple):
    ventilation_type: VentilationType
    air_flow_rate: float
    efficiency: float


class _WaterHeating(typing.NamedTuple):
    type_english: WaterHeaterType
    type_french: WaterHeaterType
    tank_volume: float
    efficiency: float


_RSI_MULTIPLIER = 5.678263337
_CFM_MULTIPLIER = 2.11888
_FEET_MULTIPLIER = 3.28084
_FEET_SQUARED_MULTIPLIER = _FEET_MULTIPLIER**2
_MILLIMETRES_TO_METRES = 1000
_LITRE_TO_GALLON = 0.264172


class HeatedFloorArea(_HeatedFloorArea):

    @classmethod
    def from_data(cls, heated_floor_area: element.Element) -> 'HeatedFloorArea':
        return HeatedFloorArea(
            area_above_grade=float(heated_floor_area.attrib['aboveGrade']),
            area_below_grade=float(heated_floor_area.attrib['belowGrade']),
        )

    @property
    def area_above_grade_feet(self):
        return self.area_above_grade * _FEET_SQUARED_MULTIPLIER

    @property
    def area_below_grade_feet(self):
        return self.area_below_grade * _FEET_SQUARED_MULTIPLIER

    def to_dict(self) -> typing.Dict[str, typing.Optional[float]]:
        return {
            'areaAboveGradeMetres': self.area_above_grade,
            'areaAboveGradeFeet': self.area_above_grade_feet,
            'areaBelowGradeMetres': self.area_below_grade,
            'areaBelowGradeFeet': self.area_below_grade_feet,
        }


class Window(_Window):

    _CODE_FIELDS = [
        'glazing_type',
        'coating_tint',
        'fill_type',
        'spacer_type',
        'window_code_type',
        'frame_material',
    ]

    @classmethod
    def from_data(cls,
                  window: element.Element,
                  window_code: typing.Dict[str, code.WindowCode]) -> 'Window':
        code_id = window.xpath('Construction/Type/@idref')
        w_code = window_code[code_id[0]] if code_id else None

        english_fields = {
            f'{field}_english': getattr(w_code, field).english if w_code else None for field in cls._CODE_FIELDS
        }
        french_fields = {
            f'{field}_french': getattr(w_code, field).french if w_code else None for field in cls._CODE_FIELDS
        }
        code_data: typing.Dict[str, typing.Any] = {}
        code_data['label'] = window.findtext('Label')
        code_data['rsi'] = float(window.xpath('Construction/Type/@rValue')[0])
        code_data['width'] = float(window.xpath('Measurements/@width')[0]) / _MILLIMETRES_TO_METRES
        code_data['height'] = float(window.xpath('Measurements/@height')[0]) / _MILLIMETRES_TO_METRES
        code_data.update(english_fields)
        code_data.update(french_fields)

        return Window(**code_data)

    @property
    def r_value(self) -> float:
        return self.rsi * _RSI_MULTIPLIER

    @property
    def area_metres(self) -> float:
        return self.width * self.height

    @property
    def area_feet(self) -> float:
        return self.area_metres * _FEET_SQUARED_MULTIPLIER

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'rsi': self.rsi,
            'rvalue': self.r_value,
            'glazingTypesEnglish': self.glazing_type_english,
            'glazingTypesFrench': self.glazing_type_french,
            'coatingsTintsEnglish': self.coating_tint_english,
            'coatingsTintsFrench': self.coating_tint_french,
            'fillTypeEnglish': self.fill_type_english,
            'fillTypeFrench': self.fill_type_french,
            'spacerTypeEnglish': self.spacer_type_english,
            'spacerTypeFrench': self.spacer_type_french,
            'typeEnglish': self.window_code_type_english,
            'typeFrench': self.window_code_type_french,
            'frameMaterialEnglish': self.frame_material_english,
            'frameMaterialFrench': self.frame_material_french,
            'areaMetres': self.area_metres,
            'areaFeet': self.area_feet,
            'width': self.width,
            'height': self.height,
        }


class Ventilation(_Ventilation):
    _VENTILATION_TRANSLATIONS = {
        VentilationType.NOT_APPLICABLE: bilingual.Bilingual(english='N/A', french='N/A'),
        VentilationType.ENERGY_STAR_INSTITUTE_CERTIFIED: bilingual.Bilingual(
            english='Home Ventilating Institute listed ENERGY STAR certified heat recovery ventilator',
            french='Ventilateur-récupérateur de chaleur répertorié par le '
                   'Home Ventilating Institute et certifié ENERGY STAR',
        ),
        VentilationType.ENERGY_STAR_NOT_INSTITUTE_CERTIFIED: bilingual.Bilingual(
            english='ENERGY STAR certified heat recovery ventilator',
            french='Ventilateur-récupérateur de chaleur certifié ENERGY STAR',
        ),
        VentilationType.NOT_ENERGY_STAR_INSTITUTE_CERTIFIED: bilingual.Bilingual(
            english='Heat recovery ventilator certified by the Home Ventilating Institute',
            french='Ventilateur-récupérateur de chaleur certifié par le Home Ventilating Institute',
        ),
        VentilationType.NOT_ENERGY_STAR_NOT_INSTITUTE_CERTIFIED: bilingual.Bilingual(
            english='Heat recovery ventilator',
            french='Ventilateur-récupérateur de chaleur',
        ),
    }

    @staticmethod
    def _derive_ventilation_type(total_supply_flow: float,
                                 energy_star: bool,
                                 institute_certified: bool) -> VentilationType:
        if total_supply_flow == 0:
            return VentilationType.NOT_APPLICABLE
        elif energy_star and institute_certified:
            return VentilationType.ENERGY_STAR_INSTITUTE_CERTIFIED
        elif energy_star and not institute_certified:
            return VentilationType.ENERGY_STAR_NOT_INSTITUTE_CERTIFIED
        elif not energy_star and institute_certified:
            return VentilationType.NOT_ENERGY_STAR_INSTITUTE_CERTIFIED
        return VentilationType.NOT_ENERGY_STAR_NOT_INSTITUTE_CERTIFIED

    @classmethod
    def from_data(cls, ventilation: element.Element) -> 'Ventilation':
        energy_star = ventilation.attrib['isEnergyStar'] == 'true'
        institute_certified = ventilation.attrib['isHomeVentilatingInstituteCertified'] == 'true'
        total_supply_flow = float(ventilation.attrib['supplyFlowrate'])

        ventilation_type = cls._derive_ventilation_type(total_supply_flow, energy_star, institute_certified)

        return Ventilation(
            ventilation_type=ventilation_type,
            air_flow_rate=total_supply_flow,
            efficiency=float(ventilation.attrib['efficiency1']),
        )

    @property
    def air_flow_rate_cmf(self):
        return self.air_flow_rate * _CFM_MULTIPLIER

    def to_dict(self) -> typing.Dict[str, typing.Union[str, float]]:
        ventilation_translation = self._VENTILATION_TRANSLATIONS[self.ventilation_type]
        return {
            'typeEnglish': ventilation_translation.english,
            'typeFrench': ventilation_translation.french,
            'airFlowRateLps': self.air_flow_rate,
            'airFlowRateCfm': self.air_flow_rate_cmf,
            'efficiency': self.efficiency,
        }


class WaterHeating(_WaterHeating):

    _TYPE_MAP = {
        ("Electricity", "Not applicable"): (
            WaterHeaterType.NOT_APPLICABLE,
            WaterHeaterType.NOT_APPLICABLE,
        ),
        ("Electricity", "Conventional tank"): (
            WaterHeaterType.ELECTRICITY_CONVENTIONAL_TANK_ENGLISH,
            WaterHeaterType.ELECTRICITY_CONVENTIONAL_TANK_FRENCH,
        ),
        ("Electricity", "Conserver tank"): (
            WaterHeaterType.ELECTRICITY_CONSERVER_TANK_ENGLISH,
            WaterHeaterType.ELECTRICITY_CONSERVER_TANK_FRENCH,
        ),
        ("Electricity", "Instantaneous"): (
            WaterHeaterType.ELECTRICITY_INSTANTANEOUS_ENGLISH,
            WaterHeaterType.ELECTRICITY_INSTANTANEOUS_FRENCH,
        ),
        ("Electricity", "Tankless heat pump"): (
            WaterHeaterType.ELECTRICITY_TANKLESS_HEAT_PUMP_ENGLISH,
            WaterHeaterType.ELECTRICITY_TANKLESS_HEAT_PUMP_FRENCH,
        ),
        ("Electricity", "Heat pump"): (
            WaterHeaterType.ELECTRICITY_HEAT_PUMP_ENGLISH,
            WaterHeaterType.ELECTRICITY_HEAT_PUMP_FRENCH,
        ),
        ("Electricity", "Add-on heat pump"): (
            WaterHeaterType.ELECTRICITY_ADDON_HEAT_PUMP_ENGLISH,
            WaterHeaterType.ELECTRICITY_ADDON_HEAT_PUMP_FRENCH,
        ),
        ("Natural gas", "Not applicable"): (
            WaterHeaterType.NOT_APPLICABLE,
            WaterHeaterType.NOT_APPLICABLE,
        ),
        ("Natural gas", "Conventional tank"): (
            WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK_ENGLISH,
            WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK_FRENCH,
        ),
        ("Natural gas", "Conventional tank (pilot)"): (
            WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK_PILOT_ENGLISH,
            WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK_PILOT_FRENCH,
        ),
        ("Natural gas", "Tankless coil"): (
            WaterHeaterType.NATURAL_GAS_TANKLESS_COIL_ENGLISH,
            WaterHeaterType.NATURAL_GAS_TANKLESS_COIL_FRENCH,
        ),
        ("Natural gas", "Instantaneous"): (
            WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_ENGLISH,
            WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_FRENCH,
        ),
        ("Natural gas", "Instantaneous (condensing)"): (
            WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_CONDENSING_ENGLISH,
            WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_CONDENSING_FRENCH,
        ),
        ("Natural gas", "Instantaneous (pilot)"): (
            WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_PILOT_ENGLISH,
            WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_PILOT_FRENCH,
        ),
        ("Natural gas", "Induced draft fan"): (
            WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN_ENGLISH,
            WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN_FRENCH,
        ),
        ("Natural gas", "Induced draft fan (pilot)"): (
            WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN_PILOT_ENGLISH,
            WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN_PILOT_FRENCH,
        ),
        ("Natural gas", "Direct vent (sealed)"): (
            WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED_ENGLISH,
            WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED_FRENCH,
        ),
        ("Natural gas", "Direct vent (sealed, pilot)"): (
            WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED_PILOT_ENGLISH,
            WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED_PILOT_FRENCH,
        ),
        ("Natural gas", "Condensing"): (
            WaterHeaterType.NATURAL_GAS_CONDENSING_ENGLISH,
            WaterHeaterType.NATURAL_GAS_CONDENSING_FRENCH,
        ),
        ("Oil", "Not applicable"): (
            WaterHeaterType.NOT_APPLICABLE,
            WaterHeaterType.NOT_APPLICABLE,
        ),
        ("Oil", "Conventional tank"): (
            WaterHeaterType.OIL_CONVENTIONAL_TANK_ENGLISH,
            WaterHeaterType.OIL_CONVENTIONAL_TANK_FRENCH,
        ),
        ("Oil", "Tankless coil"): (
            WaterHeaterType.OIL_TANKLESS_COIL_ENGLISH,
            WaterHeaterType.OIL_TANKLESS_COIL_FRENCH,
        ),
        ("Propane", "Not applicable"): (
            WaterHeaterType.NOT_APPLICABLE,
            WaterHeaterType.NOT_APPLICABLE,
        ),
        ("Propane", "Conventional tank"): (
            WaterHeaterType.PROPANE_CONVENTIONAL_TANK_ENGLISH,
            WaterHeaterType.PROPANE_CONVENTIONAL_TANK_FRENCH,
        ),
        ("Propane", "Conventional tank (pilot)"): (
            WaterHeaterType.PROPANE_CONVENTIONAL_TANK_PILOT_ENGLISH,
            WaterHeaterType.PROPANE_CONVENTIONAL_TANK_PILOT_FRENCH,
        ),
        ("Propane", "Tankless coil"): (
            WaterHeaterType.PROPANE_TANKLESS_COIL_ENGLISH,
            WaterHeaterType.PROPANE_TANKLESS_COIL_FRENCH,
        ),
        ("Propane", "Instantaneous"): (
            WaterHeaterType.PROPANE_INSTANTANEOUS_ENGLISH,
            WaterHeaterType.PROPANE_INSTANTANEOUS_FRENCH,
        ),
        ("Propane", "Instantaneous (condensing)"): (
            WaterHeaterType.PROPANE_INSTANTANEOUS_CONDENSING_ENGLISH,
            WaterHeaterType.PROPANE_INSTANTANEOUS_CONDENSING_FRENCH,
        ),
        ("Propane", "Instantaneous (pilot)"): (
            WaterHeaterType.PROPANE_INSTANTANEOUS_PILOT_ENGLISH,
            WaterHeaterType.PROPANE_INSTANTANEOUS_PILOT_FRENCH,
        ),
        ("Propane", "Induced draft fan"): (
            WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN_ENGLISH,
            WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN_FRENCH,
        ),
        ("Propane", "Induced draft fan (pilot)"): (
            WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN_PILOT_ENGLISH,
            WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN_PILOT_FRENCH,
        ),
        ("Propane", "Direct vent (sealed)"): (
            WaterHeaterType.PROPANE_DIRECT_VENT_SEALED_ENGLISH,
            WaterHeaterType.PROPANE_DIRECT_VENT_SEALED_FRENCH,
        ),
        ("Propane", "Direct vent (sealed, pilot)"): (
            WaterHeaterType.PROPANE_DIRECT_VENT_SEALED_PILOT_ENGLISH,
            WaterHeaterType.PROPANE_DIRECT_VENT_SEALED_PILOT_FRENCH,
        ),
        ("Propane", "Condensing"): (
            WaterHeaterType.PROPANE_CONDENSING_ENGLISH,
            WaterHeaterType.PROPANE_CONDENSING_FRENCH,
        ),
        ("Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)", "Not applicable"): (
            WaterHeaterType.NOT_APPLICABLE,
            WaterHeaterType.NOT_APPLICABLE,
        ),
        ("Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)", "Fireplace"): (
            WaterHeaterType.WOOD_SPACE_HEATING_FIREPLACE_ENGLISH,
            WaterHeaterType.WOOD_SPACE_HEATING_FIREPLACE_FRENCH,
        ),
        ("Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)", "Wood stove water coil"): (
            WaterHeaterType.WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL_ENGLISH,
            WaterHeaterType.WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL_FRENCH,
        ),
        ("Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)", "Indoor wood boiler"): (
            WaterHeaterType.WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER_ENGLISH,
            WaterHeaterType.WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER_FRENCH,
        ),
        ("Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)", "Outdoor wood boiler"): (
            WaterHeaterType.WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER_ENGLISH,
            WaterHeaterType.WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER_FRENCH,
        ),
        ("Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)", "Wood hot water tank"): (
            WaterHeaterType.WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK_ENGLISH,
            WaterHeaterType.WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK_FRENCH,
        ),
        ("Solar", "Solar Collector System"): (
            WaterHeaterType.SOLAR_COLLECTOR_SYSTEM_ENGLISH,
            WaterHeaterType.SOLAR_COLLECTOR_SYSTEM_FRENCH,
        ),
        ("CSA P9-11 tested Combo Heat/DHW", "CSA P9-11 tested Combo Heat/DHW"): (
            WaterHeaterType.CSA_DHW_ENGLISH,
            WaterHeaterType.CSA_DHW_FRENCH,
        ),
    }

    @classmethod
    def _from_data(cls, water_heating: element.Element) -> 'WaterHeating':
        assert water_heating.attrib['hasDrainWaterHeatRecovery'] == 'false'

        energy_type = water_heating.get_text('EnergySource/English')
        tank_type = water_heating.get_text('TankType/English')

        type_english, type_french = cls._TYPE_MAP[(energy_type, tank_type)]
        volume = float(water_heating.xpath('TankVolume/@value')[0])
        efficiency = float(water_heating.xpath('EnergyFactor/@value')[0])

        return WaterHeating(
            type_english=type_english,
            type_french=type_french,
            tank_volume=volume,
            efficiency=efficiency,
        )

    @classmethod
    def from_data(cls, water_heating: element.Element) -> typing.List['WaterHeating']:
        water_heatings = water_heating.xpath("*[self::Primary or self::Secondary]")
        return [cls._from_data(water_heating) for water_heating in water_heatings]


    @property
    def tank_volume_gallon(self):
        return self.tank_volume * _LITRE_TO_GALLON


    def to_dict(self) -> typing.Dict[str, typing.Union[str, float]]:
        return {
            'typeEnglish': self.type_english.value,
            'typeFrench': self.type_french.value,
            'tankVolumeLitres': self.tank_volume,
            'TankVolumeGallon': self.tank_volume_gallon,
            'efficiency': self.efficiency,
        }
