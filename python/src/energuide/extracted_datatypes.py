import enum
import typing
from energuide import element


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


class _Ceiling(typing.NamedTuple):
    label: str
    type_english: str
    type_french: str
    nominal_rsi: float
    effective_rsi: float
    area_metres: float
    length_metres: float


class _Floor(typing.NamedTuple):
    label: str
    nominal_rsi: float
    effective_rsi: float
    area_metres: float
    length_metres: float


class _Wall(typing.NamedTuple):
    label: str
    structure_type_english: typing.Optional[str]
    structure_type_french: typing.Optional[str]
    component_type_size_english: typing.Optional[str]
    component_type_size_french: typing.Optional[str]
    nominal_rsi: float
    effective_rsi: float
    perimeter: float
    height: float


class _Door(typing.NamedTuple):
    label: str
    type_english: str
    type_french: str
    rsi: float
    height: float
    width: float


class _Window(typing.NamedTuple):
    label: str
    glazing_types_english: typing.Optional[str]
    glazing_types_french: typing.Optional[str]
    coatings_tints_english: typing.Optional[str]
    coatings_tints_french: typing.Optional[str]
    fill_type_english: typing.Optional[str]
    fill_type_french: typing.Optional[str]
    spacer_type_english: typing.Optional[str]
    spacer_type_french: typing.Optional[str]
    type_english: typing.Optional[str]
    type_french: typing.Optional[str]
    frame_material_english: typing.Optional[str]
    frame_material_french: typing.Optional[str]
    rsi: float
    width: float
    height: float


class _HeatedFloorArea(typing.NamedTuple):
    area_above_grade: typing.Optional[float]
    area_below_grade: typing.Optional[float]


class _Ventilation(typing.NamedTuple):
    type_english: str
    type_french: str
    air_flow_rate: float
    efficiency: float


class _WallCode(typing.NamedTuple):
    identifier: str
    label: str
    structure_type_english: str
    structure_type_french: str
    component_type_size_english: str
    component_type_size_french: str


class _WindowCode(typing.NamedTuple):
    identifier: str
    label: typing.Optional[str]
    glazing_types_english: typing.Optional[str]
    glazing_types_french: typing.Optional[str]
    coatings_tints_english: typing.Optional[str]
    coatings_tints_french: typing.Optional[str]
    fill_type_english: typing.Optional[str]
    fill_type_french: typing.Optional[str]
    spacer_type_english: typing.Optional[str]
    spacer_type_french: typing.Optional[str]
    type_english: typing.Optional[str]
    type_french: typing.Optional[str]
    frame_material_english: typing.Optional[str]
    frame_material_french: typing.Optional[str]


class _WaterHeating(typing.NamedTuple):
    type_english: str
    type_french: str
    tank_volume: float
    efficiency: float


_RSI_MULTIPLIER = 5.678263337
_CFM_MULTIPLIER = 2.11888
_FEET_MULTIPLIER = 3.28084
_FEET_SQUARED_MULTIPLIER = _FEET_MULTIPLIER**2
_MILLIMETRES_TO_METRES = 1000
_LITRE_TO_USG = 0.264172


class WallCode(_WallCode):

    @classmethod
    def from_data(cls, wall_code: element.Element) -> 'WallCode':
        return WallCode(
            identifier=wall_code.attrib['id'],
            label=wall_code.get_text('Label'),
            structure_type_english=wall_code.get_text('Layers/StructureType/English'),
            structure_type_french=wall_code.get_text('Layers/StructureType/French'),
            component_type_size_english=wall_code.get_text('Layers/ComponentTypeSize/English'),
            component_type_size_french=wall_code.get_text('Layers/ComponentTypeSize/French'),
        )


class WindowCode(_WindowCode):

    @classmethod
    def from_data(cls, window_code: element.Element) -> 'WindowCode':
        return WindowCode(
            identifier=window_code.attrib['id'],
            label=window_code.findtext('Label'),
            glazing_types_english=window_code.findtext('Layers/GlazingTypes/English'),
            glazing_types_french=window_code.findtext('Layers/GlazingTypes/French'),
            coatings_tints_english=window_code.findtext('Layers/CoatingsTints/English'),
            coatings_tints_french=window_code.findtext('Layers/CoatingsTints/French'),
            fill_type_english=window_code.findtext('Layers/FillType/English'),
            fill_type_french=window_code.findtext('Layers/FillType/French'),
            spacer_type_english=window_code.findtext('Layers/SpacerType/English'),
            spacer_type_french=window_code.findtext('Layers/SpacerType/French'),
            type_english=window_code.findtext('Layers/Type/English'),
            type_french=window_code.findtext('Layers/Type/French'),
            frame_material_english=window_code.findtext('Layers/FrameMaterial/English'),
            frame_material_french=window_code.findtext('Layers/FrameMaterial/French'),
        )


class _Codes(typing.NamedTuple):
    wall: typing.Dict[str, WallCode]
    window: typing.Dict[str, WindowCode]


class Codes(_Codes):

    @classmethod
    def from_data(cls, codes: typing.Dict[str, typing.List[element.Element]]) -> 'Codes':
        wall_code_list = [WallCode.from_data(wall_code) for wall_code in codes['wall']]
        window_code_list = [WindowCode.from_data(window_code) for window_code in codes['window']]

        wall_codes = {wall_code.identifier: wall_code for wall_code in wall_code_list}
        window_codes = {window_code.identifier: window_code for window_code in window_code_list}

        return Codes(
            wall=wall_codes,
            window=window_codes,
        )


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
        'glazing_types_english',
        'glazing_types_english',
        'glazing_types_french',
        'coatings_tints_english',
        'coatings_tints_french',
        'fill_type_english',
        'fill_type_french',
        'spacer_type_english',
        'spacer_type_french',
        'type_english',
        'type_french',
        'frame_material_english',
        'frame_material_french',
    ]

    @classmethod
    def from_data(cls,
                  window: element.Element,
                  window_code: typing.Dict[str, WindowCode]) -> 'Window':
        code_id = window.xpath('Construction/Type/@idref')
        code = window_code[code_id[0]] if code_id else None

        code_data = {field: getattr(code, field) if code else None for field in cls._CODE_FIELDS}
        code_data['label'] = window.findtext('Label')
        code_data['rsi'] = float(window.xpath('Construction/Type/@rValue')[0])
        code_data['width'] = float(window.xpath('Measurements/@width')[0]) / _MILLIMETRES_TO_METRES
        code_data['height'] = float(window.xpath('Measurements/@height')[0]) / _MILLIMETRES_TO_METRES

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
            'glazingTypesEnglish': self.glazing_types_english,
            'glazingTypesFrench': self.glazing_types_french,
            'coatingsTintsEnglish': self.coatings_tints_english,
            'coatingsTintsFrench': self.coatings_tints_french,
            'fillTypeEnglish': self.fill_type_english,
            'fillTypeFrench': self.fill_type_french,
            'spacerTypeEnglish': self.spacer_type_english,
            'spacerTypeFrench': self.spacer_type_french,
            'typeEnglish': self.type_english,
            'typeFrench': self.type_french,
            'frameMaterialEnglish': self.frame_material_english,
            'frameMaterialFrench': self.frame_material_french,
            'areaMetres': self.area_metres,
            'areaFeet': self.area_feet,
            'width': self.width,
            'height': self.height,
        }


class Wall(_Wall):

    @classmethod
    def from_data(cls,
                  wall: element.Element,
                  wall_codes: typing.Dict[str, WallCode]) -> 'Wall':

        code_id = wall.xpath('Construction/Type/@idref')
        code: typing.Optional[WallCode] = None
        if code_id:
            code = wall_codes[code_id[0]]

        return Wall(
            label=wall.get_text('Label'),
            structure_type_english=code.structure_type_english if code else None,
            structure_type_french=code.structure_type_french if code else None,
            component_type_size_english=code.component_type_size_english if code else None,
            component_type_size_french=code.component_type_size_french if code else None,
            nominal_rsi=float(wall.xpath('Construction/Type/@nominalInsulation')[0]),
            effective_rsi=float(wall.xpath('Construction/Type/@rValue')[0]),
            perimeter=float(wall.xpath('Measurements/@perimeter')[0]),
            height=float(wall.xpath('Measurements/@height')[0]),
        )

    @property
    def nominal_r(self) -> float:
        return self.nominal_rsi * _RSI_MULTIPLIER

    @property
    def effective_r(self) -> float:
        return self.effective_rsi * _RSI_MULTIPLIER

    @property
    def area_metres(self) -> float:
        return self.perimeter * self.height

    @property
    def area_feet(self) -> float:
        return self.area_metres * _FEET_SQUARED_MULTIPLIER

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'structureTypeEnglish': self.structure_type_english,
            'structureTypeFrench': self.structure_type_french,
            'componentTypeSizeEnglish': self.component_type_size_english,
            'componentTypeSizeFrench': self.component_type_size_french,
            'nominalRsi': self.nominal_rsi,
            'nominalR': self.nominal_r,
            'effectiveRsi': self.effective_rsi,
            'effectiveR': self.effective_r,
            'areaMetres': self.area_metres,
            'areaFeet': self.area_feet,
            'perimeter': self.perimeter,
            'height': self.height,
        }


class Ceiling(_Ceiling):

    @classmethod
    def from_data(cls, ceiling: element.Element) -> 'Ceiling':
        return Ceiling(
            label=ceiling.get_text('Label'),
            type_english=ceiling.get_text('Construction/Type/English'),
            type_french=ceiling.get_text('Construction/Type/French'),
            nominal_rsi=float(ceiling.xpath('Construction/CeilingType/@nominalInsulation')[0]),
            effective_rsi=float(ceiling.xpath('Construction/CeilingType/@rValue')[0]),
            area_metres=float(ceiling.xpath('Measurements/@area')[0]),
            length_metres=float(ceiling.xpath('Measurements/@length')[0]),
        )

    @property
    def nominal_r(self) -> float:
        return self.nominal_rsi * _RSI_MULTIPLIER

    @property
    def effective_r(self) -> float:
        return self.effective_rsi * _RSI_MULTIPLIER

    @property
    def area_feet(self) -> float:
        return self.area_metres * _FEET_SQUARED_MULTIPLIER

    @property
    def length_feet(self) -> float:
        return self.length_metres * _FEET_MULTIPLIER

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'typeEnglish': self.type_english,
            'typeFrench': self.type_french,
            'nominalRsi': self.nominal_rsi,
            'nominalR': self.nominal_r,
            'effectiveRsi': self.effective_rsi,
            'effectiveR': self.effective_r,
            'areaMetres': self.area_metres,
            'areaFeet': self.area_feet,
            'lengthMetres': self.length_metres,
            'lengthFeet': self.length_feet,
        }


class Floor(_Floor):

    @classmethod
    def from_data(cls, floor: element.Element) -> 'Floor':
        return Floor(
            label=floor.get_text('Label'),
            nominal_rsi=float(floor.xpath('Construction/Type/@nominalInsulation')[0]),
            effective_rsi=float(floor.xpath('Construction/Type/@rValue')[0]),
            area_metres=float(floor.xpath('Measurements/@area')[0]),
            length_metres=float(floor.xpath('Measurements/@length')[0]),
        )

    @property
    def nominal_r(self) -> float:
        return self.nominal_rsi * _RSI_MULTIPLIER

    @property
    def effective_r(self) -> float:
        return self.effective_rsi * _RSI_MULTIPLIER

    @property
    def area_feet(self) -> float:
        return self.area_metres * _FEET_SQUARED_MULTIPLIER

    @property
    def length_feet(self) -> float:
        return self.length_metres * _FEET_MULTIPLIER

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'nominalRsi': self.nominal_rsi,
            'nominalR': self.nominal_r,
            'effectiveRsi': self.effective_rsi,
            'effectiveR': self.effective_r,
            'areaMetres': self.area_metres,
            'areaFeet': self.area_feet,
            'lengthMetres': self.length_metres,
            'lengthFeet': self.length_feet,
        }


class Door(_Door):

    @classmethod
    def from_data(cls, door: element.Element) -> 'Door':
        return Door(
            label=door.get_text('Label'),
            type_english=door.get_text('Construction/Type/English'),
            type_french=door.get_text('Construction/Type/French'),
            rsi=float(door.xpath('Construction/Type/@value')[0]),
            height=float(door.xpath('Measurements/@height')[0]),
            width=float(door.xpath('Measurements/@width')[0]),
        )

    @property
    def r_value(self) -> float:
        return self.rsi * _RSI_MULTIPLIER

    @property
    def u_factor(self) -> float:
        return 1 / self.rsi

    @property
    def u_factor_imperial(self) -> float:
        return self.u_factor / _RSI_MULTIPLIER

    @property
    def area_metres(self) -> float:
        return self.height * self.width

    @property
    def area_feet(self) -> float:
        return self.area_metres * _FEET_SQUARED_MULTIPLIER

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'typeEnglish': self.type_english,
            'typeFrench': self.type_french,
            'rsi': self.rsi,
            'rValue': self.r_value,
            'uFactor': self.u_factor,
            'uFactorImperial': self.u_factor_imperial,
            'areaMetres': self.area_metres,
            'areaFeet': self.area_feet,
        }


class Ventilation(_Ventilation):

    @classmethod
    def _derive_type_string(cls, energy_star: bool, institute_certified: bool) -> typing.Tuple[str, str]:
        if energy_star and institute_certified:
            return ('Home Ventilating Institute listed ENERGY STAR certified heat recovery ventilator',
                    'Ventilateur-récupérateur de chaleur répertorié par le Home Ventilating Institute ' + \
                    'et certifiéENERGY STAR')
        elif energy_star and not institute_certified:
            return ('ENERGY STAR certified heat recovery ventilator',
                    'Ventilateur-récupérateur de chaleur certifié ENERGY STAR')
        elif not energy_star and institute_certified:
            return ('Heat recovery ventilator certified by the Home Ventilating Institute',
                    'Ventilateur-récupérateur de chaleur certifié par le Home Ventilating Institute')
        return ('Heat recovery ventilator', 'Ventilateur-récupérateur de chaleur')


    @classmethod
    def from_data(cls, ventilation: element.Element) -> 'Ventilation':
        energy_star = ventilation.attrib['isEnergyStar'] == 'true'
        institute_certified = ventilation.attrib['isHomeVentilatingInstituteCertified'] == 'true'
        total_supply_flow = float(ventilation.attrib['supplyFlowrate'])

        if total_supply_flow == 0:
            type_english, type_french = 'N/A', 'N/A'
        else:
            type_english, type_french = cls._derive_type_string(energy_star, institute_certified)

        return Ventilation(
            type_english=type_english,
            type_french=type_french,
            air_flow_rate=total_supply_flow,
            efficiency=float(ventilation.attrib['efficiency1']),
        )

    @property
    def air_flow_rate_cmf(self):
        return self.air_flow_rate * _CFM_MULTIPLIER

    def to_dict(self) -> typing.Dict[str, typing.Union[str, float]]:
        return {
            'typeEnglish': self.type_english,
            'typeFrench': self.type_french,
            'airFlowRateLps': self.air_flow_rate,
            'airFlowRateCfm': self.air_flow_rate_cmf,
            'efficiency': self.efficiency,
        }


class WaterHeating(_WaterHeating):

    _TYPE_MAP = {
        ("Electricity", "Not applicable"): (
            WaterHeaterType.NOT_APPLICABLE.value,
            WaterHeaterType.NOT_APPLICABLE.value,
        ),
        ("Electricity", "Conventional tank"): (
            WaterHeaterType.ELECTRICITY_CONVENTIONAL_TANK_ENGLISH.value,
            WaterHeaterType.ELECTRICITY_CONVENTIONAL_TANK_FRENCH.value,
        ),
        ("Electricity", "Conserver tank"): (
            WaterHeaterType.ELECTRICITY_CONSERVER_TANK_ENGLISH.value,
            WaterHeaterType.ELECTRICITY_CONSERVER_TANK_FRENCH.value,
        ),
        ("Electricity", "Instantaneous"): (
            WaterHeaterType.ELECTRICITY_INSTANTANEOUS_ENGLISH.value,
            WaterHeaterType.ELECTRICITY_INSTANTANEOUS_FRENCH.value,
        ),
        ("Electricity", "Tankless heat pump"): (
            WaterHeaterType.ELECTRICITY_TANKLESS_HEAT_PUMP_ENGLISH.value,
            WaterHeaterType.ELECTRICITY_TANKLESS_HEAT_PUMP_FRENCH.value,
        ),
        ("Electricity", "Heat pump"): (
            WaterHeaterType.ELECTRICITY_HEAT_PUMP_ENGLISH.value,
            WaterHeaterType.ELECTRICITY_HEAT_PUMP_FRENCH.value,
        ),
        ("Electricity", "Add-on heat pump"): (
            WaterHeaterType.ELECTRICITY_ADDON_HEAT_PUMP_ENGLISH.value,
            WaterHeaterType.ELECTRICITY_ADDON_HEAT_PUMP_FRENCH.value,
        ),
        ("Natural gas", "Not applicable"): (
            WaterHeaterType.NOT_APPLICABLE.value,
            WaterHeaterType.NOT_APPLICABLE.value,
        ),
        ("Natural gas", "Conventional tank"): (
            WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK_ENGLISH.value,
            WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK_FRENCH.value,
        ),
        ("Natural gas", "Conventional tank (pilot)"): (
            WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK_PILOT_ENGLISH.value,
            WaterHeaterType.NATURAL_GAS_CONVENTIONAL_TANK_PILOT_FRENCH.value,
        ),
        ("Natural gas", "Tankless coil"): (
            WaterHeaterType.NATURAL_GAS_TANKLESS_COIL_ENGLISH.value,
            WaterHeaterType.NATURAL_GAS_TANKLESS_COIL_FRENCH.value,
        ),
        ("Natural gas", "Instantaneous"): (
            WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_ENGLISH.value,
            WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_FRENCH.value,
        ),
        ("Natural gas", "Instantaneous (condensing)"): (
            WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_CONDENSING_ENGLISH.value,
            WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_CONDENSING_FRENCH.value,
        ),
        ("Natural gas", "Instantaneous (pilot)"): (
            WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_PILOT_ENGLISH.value,
            WaterHeaterType.NATURAL_GAS_INSTANTANEOUS_PILOT_FRENCH.value,
        ),
        ("Natural gas", "Induced draft fan"): (
            WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN_ENGLISH.value,
            WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN_FRENCH.value,
        ),
        ("Natural gas", "Induced draft fan (pilot)"): (
            WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN_PILOT_ENGLISH.value,
            WaterHeaterType.NATURAL_GAS_INDUCED_DRAFT_FAN_PILOT_FRENCH.value,
        ),
        ("Natural gas", "Direct vent (sealed)"): (
            WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED_ENGLISH.value,
            WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED_FRENCH.value,
        ),
        ("Natural gas", "Direct vent (sealed, pilot)"): (
            WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED_PILOT_ENGLISH.value,
            WaterHeaterType.NATURAL_GAS_DIRECT_VENT_SEALED_PILOT_FRENCH.value,
        ),
        ("Natural gas", "Condensing"): (
            WaterHeaterType.NATURAL_GAS_CONDENSING_ENGLISH.value,
            WaterHeaterType.NATURAL_GAS_CONDENSING_FRENCH.value,
        ),
        ("Oil", "Not applicable"): (
            WaterHeaterType.NOT_APPLICABLE.value,
            WaterHeaterType.NOT_APPLICABLE.value,
        ),
        ("Oil", "Conventional tank"): (
            WaterHeaterType.OIL_CONVENTIONAL_TANK_ENGLISH.value,
            WaterHeaterType.OIL_CONVENTIONAL_TANK_FRENCH.value,
        ),
        ("Oil", "Tankless coil"): (
            WaterHeaterType.OIL_TANKLESS_COIL_ENGLISH.value,
            WaterHeaterType.OIL_TANKLESS_COIL_FRENCH.value,
        ),
        ("Propane", "Not applicable"): (
            WaterHeaterType.NOT_APPLICABLE.value,
            WaterHeaterType.NOT_APPLICABLE.value,
        ),
        ("Propane", "Conventional tank"): (
            WaterHeaterType.PROPANE_CONVENTIONAL_TANK_ENGLISH.value,
            WaterHeaterType.PROPANE_CONVENTIONAL_TANK_FRENCH.value,
        ),
        ("Propane", "Conventional tank (pilot)"): (
            WaterHeaterType.PROPANE_CONVENTIONAL_TANK_PILOT_ENGLISH.value,
            WaterHeaterType.PROPANE_CONVENTIONAL_TANK_PILOT_FRENCH.value,
        ),
        ("Propane", "Tankless coil"): (
            WaterHeaterType.PROPANE_TANKLESS_COIL_ENGLISH.value,
            WaterHeaterType.PROPANE_TANKLESS_COIL_FRENCH.value,
        ),
        ("Propane", "Instantaneous"): (
            WaterHeaterType.PROPANE_INSTANTANEOUS_ENGLISH.value,
            WaterHeaterType.PROPANE_INSTANTANEOUS_FRENCH.value,
        ),
        ("Propane", "Instantaneous (condensing)"): (
            WaterHeaterType.PROPANE_INSTANTANEOUS_CONDENSING_ENGLISH.value,
            WaterHeaterType.PROPANE_INSTANTANEOUS_CONDENSING_FRENCH.value,
        ),
        ("Propane", "Instantaneous (pilot)"): (
            WaterHeaterType.PROPANE_INSTANTANEOUS_PILOT_ENGLISH.value,
            WaterHeaterType.PROPANE_INSTANTANEOUS_PILOT_FRENCH.value,
        ),
        ("Propane", "Induced draft fan"): (
            WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN_ENGLISH.value,
            WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN_FRENCH.value,
        ),
        ("Propane", "Induced draft fan (pilot)"): (
            WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN_PILOT_ENGLISH.value,
            WaterHeaterType.PROPANE_INDUCED_DRAFT_FAN_PILOT_FRENCH.value,
        ),
        ("Propane", "Direct vent (sealed)"): (
            WaterHeaterType.PROPANE_DIRECT_VENT_SEALED_ENGLISH.value,
            WaterHeaterType.PROPANE_DIRECT_VENT_SEALED_FRENCH.value,
        ),
        ("Propane", "Direct vent (sealed, pilot)"): (
            WaterHeaterType.PROPANE_DIRECT_VENT_SEALED_PILOT_ENGLISH.value,
            WaterHeaterType.PROPANE_DIRECT_VENT_SEALED_PILOT_FRENCH.value,
        ),
        ("Propane", "Condensing"): (
            WaterHeaterType.PROPANE_CONDENSING_ENGLISH.value,
            WaterHeaterType.PROPANE_CONDENSING_FRENCH.value,
        ),
        ("Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)", "Not applicable"): (
            WaterHeaterType.NOT_APPLICABLE.value,
            WaterHeaterType.NOT_APPLICABLE.value,
        ),
        ("Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)", "Fireplace"): (
            WaterHeaterType.WOOD_SPACE_HEATING_FIREPLACE_ENGLISH.value,
            WaterHeaterType.WOOD_SPACE_HEATING_FIREPLACE_FRENCH.value,
        ),
        ("Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)", "Wood stove water coil"): (
            WaterHeaterType.WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL_ENGLISH.value,
            WaterHeaterType.WOOD_SPACE_HEATING_WOOD_STOVE_WATER_COIL_FRENCH.value,
        ),
        ("Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)", "Indoor wood boiler"): (
            WaterHeaterType.WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER_ENGLISH.value,
            WaterHeaterType.WOOD_SPACE_HEATING_INDOOR_WOOD_BOILER_FRENCH.value,
        ),
        ("Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)", "Outdoor wood boiler"): (
            WaterHeaterType.WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER_ENGLISH.value,
            WaterHeaterType.WOOD_SPACE_HEATING_OUTDOOR_WOOD_BOILER_FRENCH.value,
        ),
        ("Wood Space Heating (Mixed Wood, Hardwood, Soft Wood or Wood Pellets)", "Wood hot water tank"): (
            WaterHeaterType.WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK_ENGLISH.value,
            WaterHeaterType.WOOD_SPACE_HEATING_WOOD_HOT_WATER_TANK_FRENCH.value,
        ),
        ("Solar", "Solar Collector System"): (
            WaterHeaterType.SOLAR_COLLECTOR_SYSTEM_ENGLISH.value,
            WaterHeaterType.SOLAR_COLLECTOR_SYSTEM_FRENCH.value,
        ),
        ("CSA P9-11 tested Combo Heat/DHW", "CSA P9-11 tested Combo Heat/DHW"): (
            WaterHeaterType.CSA_DHW_ENGLISH.value,
            WaterHeaterType.CSA_DHW_FRENCH.value,
        ),
    }

    @classmethod
    def _from_data(cls, water_heating: element.Element) -> 'WaterHeating':
        assert water_heating.attrib['hasDrainWaterHeatRecovery'] == 'false'

        energy_type = water_heating.xpath('EnergySource/English/text()')[0]
        tank_type = water_heating.xpath('TankType/English/text()')[0]

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
    def tank_volume_usg(self):
        return self.tank_volume * _LITRE_TO_USG


    def to_dict(self) -> typing.Dict[str, typing.Union[str, float]]:
        return {
            'typeEnglish': self.type_english,
            'typeFrench': self.type_french,
            'tankVolumeLitres': self.tank_volume,
            'TankVolumeUsg': self.tank_volume_usg,
            'efficiency': self.efficiency,
        }
