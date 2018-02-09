import typing
from energuide import element


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
    rsi: typing.Optional[float]
    width: typing.Optional[float]
    height: typing.Optional[float]


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
    label: typing.Optional[str]
    structure_type_english: typing.Optional[str]
    structure_type_french: typing.Optional[str]
    component_type_size_english: typing.Optional[str]
    component_type_size_french: typing.Optional[str]


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


_RSI_MULTIPLIER = 5.678263337
_CFM_MULTIPLIER = 2.11888
_FEET_MULTIPLIER = 3.28084
_FEET_SQUARED_MULTIPLIER = _FEET_MULTIPLIER**2


class WallCode(_WallCode):

    SCHEMA = {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'type': 'string', 'required': True},
                'label': {'type': 'string', 'required': True, 'nullable': True},
                'structureTypeEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'structureTypeFrench': {'type': 'string', 'required': True, 'nullable': True},
                'componentTypeSizeEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'componentTypeSizeFrench': {'type': 'string', 'required': True, 'nullable': True},
            }
        }
    }

    @classmethod
    def from_data(cls, wall_code: typing.Dict[str, typing.Optional[str]]) -> 'WallCode':
        return WallCode(
            identifier=wall_code['id'],
            label=wall_code['label'],
            structure_type_english=wall_code['structureTypeEnglish'],
            structure_type_french=wall_code['structureTypeFrench'],
            component_type_size_english=wall_code['componentTypeSizeEnglish'],
            component_type_size_french=wall_code['componentTypeSizeFrench'],
        )


class WindowCode(_WindowCode):

    SCHEMA = {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'id':  {'type': 'string', 'required': True},
                'label': {'type': 'string', 'required': True, 'nullable': True},
                'glazingTypesEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'glazingTypesFrench': {'type': 'string', 'required': True, 'nullable': True},
                'coatingsTintsEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'coatingsTintsFrench': {'type': 'string', 'required': True, 'nullable': True},
                'fillTypeEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'fillTypeFrench': {'type': 'string', 'required': True, 'nullable': True},
                'spacerTypeEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'spacerTypeFrench': {'type': 'string', 'required': True, 'nullable': True},
                'typeEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'typeFrench': {'type': 'string', 'required': True, 'nullable': True},
                'frameMaterialEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'frameMaterialFrench': {'type': 'string', 'required': True, 'nullable': True},
            }
        }
    }

    @classmethod
    def from_data(cls, wall_code: typing.Dict[str, typing.Optional[str]]) -> 'WindowCode':
        return WindowCode(
            identifier=wall_code['id'],
            label=wall_code['label'],
            glazing_types_english=wall_code['glazingTypesEnglish'],
            glazing_types_french=wall_code['glazingTypesFrench'],
            coatings_tints_english=wall_code['coatingsTintsEnglish'],
            coatings_tints_french=wall_code['coatingsTintsFrench'],
            fill_type_english=wall_code['fillTypeEnglish'],
            fill_type_french=wall_code['fillTypeFrench'],
            spacer_type_english=wall_code['spacerTypeEnglish'],
            spacer_type_french=wall_code['spacerTypeFrench'],
            type_english=wall_code['typeEnglish'],
            type_french=wall_code['typeFrench'],
            frame_material_english=wall_code['frameMaterialEnglish'],
            frame_material_french=wall_code['frameMaterialFrench'],
        )


class _Codes(typing.NamedTuple):
    wall: typing.Dict[str, WallCode]
    window: typing.Dict[str, WindowCode]


class Codes(_Codes):

    SCHEMA = {
        'type': 'dict',
        'required': True,
        'schema': {
            'wall': WallCode.SCHEMA,
            'window': WindowCode.SCHEMA,
        }
    }

    @classmethod
    def from_data(cls, codes: typing.Dict[str, typing.List[typing.Dict[str, str]]]):
        wall_code_list = (WallCode.from_data(wall_code) for wall_code in codes['wall'])
        window_code_list = (WindowCode.from_data(window_code) for window_code in codes['window'])

        wall_codes = {wall_code.identifier: wall_code for wall_code in wall_code_list}
        window_codes = {window_code.identifier: window_code for window_code in window_code_list}

        return Codes(
            wall=wall_codes,
            window=window_codes,
        )


class HeatedFloorArea(_HeatedFloorArea):

    SCHEMA = {
        'type': 'dict',
        'required': True,
        'schema': {
            'belowGrade': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
            'aboveGrade': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
        }
    }

    @classmethod
    def from_data(cls, heated_floor_area: typing.Dict[str, typing.Optional[float]]) -> 'HeatedFloorArea':
        return HeatedFloorArea(
            area_above_grade=heated_floor_area['aboveGrade'],
            area_below_grade=heated_floor_area['belowGrade'],
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

    SCHEMA = {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'label': {'type': 'string', 'required': True, 'nullable': True},
                'constructionTypeCode': {'type': 'string', 'required': False, 'nullable': True},
                'constructionTypeValue': {'type': 'string', 'required': False, 'nullable': True},
                'rsi': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
                'width': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
                'height': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
            }
        }
    }

    @classmethod
    def from_data(cls,
                  window: typing.Dict[str, typing.Any],
                  window_code: typing.Dict[str, WindowCode]) -> 'Window':
        code_id = window.get('constructionTypeCode')
        code = window_code.get(code_id)

        glazing_types_english = code.glazing_types_english if code is not None else None
        glazing_types_french = code.glazing_types_french if code is not None else None
        coatings_tints_english = code.coatings_tints_english if code is not None else None
        coatings_tints_french = code.coatings_tints_french if code is not None else None
        fill_type_english = code.fill_type_english if code is not None else None
        fill_type_french = code.fill_type_french if code is not None else None
        spacer_type_english = code.spacer_type_english if code is not None else None
        spacer_type_french = code.spacer_type_french if code is not None else None
        type_english = code.type_english if code is not None else None
        type_french = code.type_french if code is not None else None
        frame_material_english = code.frame_material_english if code is not None else None
        frame_material_french = code.frame_material_french if code is not None else None

        return Window(
            label=window['label'],
            glazing_types_english=glazing_types_english,
            glazing_types_french=glazing_types_french,
            coatings_tints_english=coatings_tints_english,
            coatings_tints_french=coatings_tints_french,
            fill_type_english=fill_type_english,
            fill_type_french=fill_type_french,
            spacer_type_english=spacer_type_english,
            spacer_type_french=spacer_type_french,
            type_english=type_english,
            type_french=type_french,
            frame_material_english=frame_material_english,
            frame_material_french=frame_material_french,
            rsi=window['rsi'],
            width=(window['width'] * 0.001) if (window['width'] is not None) else None,
            height=(window['height']* 0.001) if (window['height'] is not None) else None,
        )

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'rsi': self.rsi,
            'rvalue': (self.rsi * _RSI_MULTIPLIER) if (self.rsi is not None) else None,
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
            'areaMetres': self.width * self.height,
            'areaFeet': (self.width * self.height * _FEET_SQUARED_MULTIPLIER)
                        if (self.width is not None and self.height is not None) else None,
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
            label=wall.findtext('Label'),
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
            label=ceiling.findtext('Label'),
            type_english=ceiling.findtext('Construction/Type/English'),
            type_french=ceiling.findtext('Construction/Type/French'),
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
            label=floor.findtext('Label'),
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
            label=door.findtext('Label'),
            type_english=door.findtext('Construction/Type/English'),
            type_french=door.findtext('Construction/Type/French'),
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
    _TYPE_MAP = {
        'false': {
            'false': ('Heat recovery ventilator', 'Ventilateur-récupérateur de chaleur'),
            'true': ('Heat recovery ventilator certified by the Home Ventilating Institute',
                     'Ventilateur-récupérateur de chaleur certifié par le Home Ventilating Institute'),
        },
        'true': {
            'false': ('ENERGY STAR certified heat recovery ventilator',
                      'Ventilateur-récupérateur de chaleur certifié ENERGY STAR'),
            'true': ('Home Ventilating Institute listed ENERGY STAR certified heat recovery ventilator',
                     'Ventilateur-récupérateur de chaleur répertorié par le Home Ventilating Institute et certifié\
ENERGY STAR'),
        }
    }

    @classmethod
    def _derive_type_string(cls, energy_star: bool, institute_certified: bool) -> str:
        if energy_star and institute_certified:
            return ('Home Ventilating Institute listed ENERGY STAR certified heat recovery ventilator',
                    'Ventilateur-récupérateur de chaleur répertorié par le Home Ventilating Institute \
et certifiéENERGY STAR')
        elif energy_star and not institute_certified:
            return ('ENERGY STAR certified heat recovery ventilator',
                    'Ventilateur-récupérateur de chaleur certifié ENERGY STAR')
        elif not energy_star and institute_certified:
            return ('Heat recovery ventilator certified by the Home Ventilating Institute',
                    'Ventilateur-récupérateur de chaleur certifié par le Home Ventilating Institute')
        else:
            return ('Heat recovery ventilator', 'Ventilateur-récupérateur de chaleur')


    @classmethod
    def from_data(cls, ventilation: element.Element) -> 'Ventilation':
        energy_star = ventilation.xpath('@isEnergyStar')[0] == 'true'
        institute_certified = ventilation.xpath('@isHomeVentilatingInstituteCertified')[0] == 'true'
        total_supply_flow = float(ventilation.xpath('@supplyFlowrate')[0])

        if total_supply_flow == 0:
            type_english, type_french = 'N/A', 'N/A'
        else:
            type_english, type_french = cls._derive_type_string(energy_star, institute_certified)

        return Ventilation(
            type_english=type_english,
            type_french=type_french,
            air_flow_rate=total_supply_flow,
            efficiency=float(ventilation.xpath('@efficiency1')[0]),
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
