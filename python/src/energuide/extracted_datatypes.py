import enum
import typing
from energuide import element


_RSI_MULTIPLIER = 5.678263337
_CFM_MULTIPLIER = 2.11888
_FEET_MULTIPLIER = 3.28084
_FEET_SQUARED_MULTIPLIER = _FEET_MULTIPLIER**2
_MILLIMETRES_TO_METRES = 1000
_KWH_TO_BTU = 3412.142


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


@enum.unique
class HeatingType(enum.Enum):
    FURNACE = 'Furnace'


@enum.unique
class Language(enum.Enum):
    ENGLISH = enum.auto()
    FRENCH = enum.auto()


class Translations:

    def __init__(self, versions: typing.Dict[Language, str]) -> None:
        self._versions = versions

    def to_string(self, language: Language) -> str:
        return self._versions[language]


@enum.unique
class EnergySource(enum.Enum):
    NATURAL_GAS = Translations({
        Language.ENGLISH: 'Natural Gas',
        Language.FRENCH: 'Chauffage au gaz naturel',
    })


class HeatingFullType(enum.Enum):
    FURNACE_NG_CONTINUOUS_PILOT = Translations({
        Language.ENGLISH: 'Natural gas furnace with pilot',
        Language.FRENCH: 'Générateur d’air chaud au gaz naturel avec veilleuse',
    })


class _Heating(typing.NamedTuple):
    label: str
    energy_source: EnergySource
    heating_type: HeatingType
    equipment_type: HeatingFullType
    output_size: float
    efficiency: float
    steady_state: str


class Heating(_Heating):

    _ENERGY_SOURCES = {
        2: EnergySource.NATURAL_GAS
    }

    _EQUIPMENT_TYPES = {
        (HeatingType.FURNACE, EnergySource.NATURAL_GAS, 1): HeatingFullType.FURNACE_NG_CONTINUOUS_PILOT,
    }

    @staticmethod
    def calculate_output_size(heating_type_node: element.Element) -> float:
        measurement = float(heating_type_node.xpath('Specifications/OutputCapacity/@value')[0])
        units = heating_type_node.xpath('Specifications/OutputCapacity/@uiUnits')[0]
        return measurement / _KWH_TO_BTU if units == 'btu/hr' else measurement

    @classmethod
    def from_data(cls, heating_node: element.Element) -> 'Heating':
        label = heating_node.get_text('Label')

        heating_type_node = heating_node.xpath('Type1/*[self::Baseboards or self::Furnace or self::Boiler]')[0]
        heating_type = HeatingType(heating_type_node.tag)

        energy_source_code = int(heating_type_node.xpath('Equipment/EnergySource/@code')[0])
        energy_source = cls._ENERGY_SOURCES[energy_source_code]

        equipment_type_code = int(heating_type_node.xpath('Equipment/EquipmentType/@code')[0])
        equipment_type = cls._EQUIPMENT_TYPES[heating_type, energy_source, equipment_type_code]

        efficiency = float(heating_type_node.xpath('Specifications/@efficiency')[0])
        output_size = cls.calculate_output_size(heating_type_node)

        steady_state_flag = heating_type_node.xpath('Specifications/@isSteadyState')[0]
        steady_state = 'Steady State' if steady_state_flag == 'true' else 'AFUE'

        return Heating(
            label=label,
            energy_source=energy_source,
            heating_type=heating_type,
            equipment_type=equipment_type,
            output_size=output_size,
            efficiency=efficiency,
            steady_state=steady_state,
        )


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
