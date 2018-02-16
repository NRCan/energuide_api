import enum
import typing
from energuide import element
from energuide import bilingual


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


_RSI_MULTIPLIER = 5.678263337
_CFM_MULTIPLIER = 2.11888
_FEET_MULTIPLIER = 3.28084
_FEET_SQUARED_MULTIPLIER = _FEET_MULTIPLIER**2
_MILLIMETRES_TO_METRES = 1000

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
