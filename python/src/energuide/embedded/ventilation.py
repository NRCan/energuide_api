import enum
import typing
from energuide import element
from energuide import bilingual
from energuide.exceptions import InvalidEmbeddedDataTypeException


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


class Ventilation(_Ventilation):

    _CFM_MULTIPLIER = 2.11888

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
        try:
            energy_star = ventilation.attrib['isEnergyStar'] == 'true'
            institute_certified = ventilation.attrib['isHomeVentilatingInstituteCertified'] == 'true'
            total_supply_flow = float(ventilation.attrib['supplyFlowrate'])

            ventilation_type = cls._derive_ventilation_type(total_supply_flow, energy_star, institute_certified)

            return Ventilation(
                ventilation_type=ventilation_type,
                air_flow_rate=total_supply_flow,
                efficiency=float(ventilation.attrib['efficiency1']),
            )
        except (KeyError, ValueError) as exc:
            raise InvalidEmbeddedDataTypeException(Ventilation) from exc

    @property
    def air_flow_rate_cmf(self):
        return self.air_flow_rate * self._CFM_MULTIPLIER

    def to_dict(self) -> typing.Dict[str, typing.Union[str, float]]:
        ventilation_translation = self._VENTILATION_TRANSLATIONS[self.ventilation_type]
        return {
            'typeEnglish': ventilation_translation.english,
            'typeFrench': ventilation_translation.french,
            'airFlowRateLps': self.air_flow_rate,
            'airFlowRateCfm': self.air_flow_rate_cmf,
            'efficiency': self.efficiency,
        }
