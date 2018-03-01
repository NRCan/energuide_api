import enum
import typing
from energuide import bilingual
from energuide import element
from energuide.exceptions import InvalidEmbeddedDataTypeError


class HeatingType(enum.Enum):
    BASEBOARD = enum.auto()
    FURNACE = enum.auto()
    BOILER = enum.auto()
    COMBO_HEAT_DHW = enum.auto()
    P911 = enum.auto()


class EnergySource(enum.Enum):
    ELECTRIC = enum.auto()
    NATURAL_GAS = enum.auto()
    OIL = enum.auto()
    PROPANE = enum.auto()
    WOOD = enum.auto()
    HARDWOOD = enum.auto()


class _Heating(typing.NamedTuple):
    heating_type: HeatingType
    energy_source: EnergySource
    equipment_type: bilingual.Bilingual
    label: str
    output_size: float
    efficiency: float
    steady_state: str


class Heating(_Heating):

    _KWH_TO_BTU = 3412.142

    _HEATING_TYPE_NODE_NAMES = {
        'Baseboards': HeatingType.BASEBOARD,
        'Furnace': HeatingType.FURNACE,
        'Boiler': HeatingType.BOILER,
    }

    _HEATING_TYPE_TRANSLATIONS = {
        HeatingType.BASEBOARD: bilingual.Bilingual(english='Electric baseboard',
                                                   french='Plinthe électrique'),
        HeatingType.FURNACE: bilingual.Bilingual(english='Furnace', french='Fournaise'),
        HeatingType.BOILER: bilingual.Bilingual(english='Boiler', french='Chaudière'),
        HeatingType.COMBO_HEAT_DHW: bilingual.Bilingual(english='Combo Heat/DHW',
                                                        french='Combinaison chaleur/ Eau Chaude Domestique'),
        HeatingType.P911: bilingual.Bilingual(english='Certified combo system, space and domestic water heating',
                                              french='Système combiné certifié pour le chauffage '
                                                     'des locaux et de l’eau'),
    }

    _ENERGY_SOURCE_CODES = {
        1: EnergySource.ELECTRIC,
        2: EnergySource.NATURAL_GAS,
        3: EnergySource.OIL,
        4: EnergySource.PROPANE,
        5: EnergySource.WOOD,
        6: EnergySource.WOOD,
    }

    _ENERGY_SOURCE_TRANSLATIONS = {
        EnergySource.ELECTRIC: bilingual.Bilingual(english='Electric Space Heating',
                                                   french='Chauffage électrique'),
        EnergySource.NATURAL_GAS: bilingual.Bilingual(english='Natural Gas', french='Chauffage au gaz naturel'),
        EnergySource.OIL: bilingual.Bilingual(english='Oil Space Heating', french='Chauffage au mazout'),
        EnergySource.PROPANE: bilingual.Bilingual(english='Propane Space Heating', french='Chauffage au propane'),
        EnergySource.WOOD: bilingual.Bilingual(english='Wood Space Heating (Mixed Wood, Hardwood, '
                                                       'Soft Wood or Wood Pellets)',
                                               french='Chauffage au bois(Bois mélangé, Bois dur, Bois mou, '
                                                      'Granules de bois)')
    }

    @classmethod
    def _get_output_size(cls, node: element.Element) -> float:
        capacity_node = node.find('Type1/*/Specifications/OutputCapacity')
        assert capacity_node is not None

        units = capacity_node.attrib['uiUnits']
        capacity_value = float(capacity_node.attrib['value'])
        capacity: typing.Optional[float]
        if units == 'kW':
            capacity = capacity_value
        elif units == 'btu/hr':
            capacity = capacity_value / cls._KWH_TO_BTU
        else:
            raise InvalidEmbeddedDataTypeError(
                Heating, f'Unknown capacity units: {units}')
        assert capacity is not None
        return capacity

    @classmethod
    def _get_heating_type(cls, node: element.Element) -> HeatingType:
        candidates = [candidate.tag for candidate in node.xpath('Type1/*')]
        heating_type: typing.Optional[HeatingType] = None
        for candidate in candidates:
            if candidate in cls._HEATING_TYPE_NODE_NAMES:
                heating_type = cls._HEATING_TYPE_NODE_NAMES[candidate]
                break
        if heating_type is None:
            raise InvalidEmbeddedDataTypeError(
                Heating, f'Could not identify HeatingType, candidate node names = {[candidates]}')
        return heating_type

    @classmethod
    def _get_energy_source(cls, node: element.Element) -> EnergySource:
        code = node.get('Type1/*/Equipment/EnergySource/@code', int)
        energy_source = cls._ENERGY_SOURCE_CODES.get(code)
        if energy_source is None:
            raise InvalidEmbeddedDataTypeError(
                Heating, f'Unknown energy source: {energy_source}')
        return energy_source

    @classmethod
    def _get_equipment_type(cls, node: element.Element) -> bilingual.Bilingual:
        english_text = node.get_text('Type1/*/Equipment/EquipmentType/English')
        french_text = node.get_text('Type1/*/Equipment/EquipmentType/French')
        return bilingual.Bilingual(english=english_text, french=french_text)

    @staticmethod
    def _get_steady_state(node: element.Element) -> str:
        steady_state_value = node.get('Type1/*/Specifications/@isSteadyState', str)
        return 'Steady State' if steady_state_value == 'true' else 'AFUE'

    @classmethod
    def from_data(cls, node: element.Element) -> 'Heating':
        return Heating(
            label=node.get_text('Label'),
            output_size=float(Heating._get_output_size(node)),
            efficiency=node.get('Type1/*/Specifications/@efficiency', float),
            steady_state=cls._get_steady_state(node),
            heating_type=cls._get_heating_type(node),
            energy_source=cls._get_energy_source(node),
            equipment_type=cls._get_equipment_type(node),
        )

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'heatingTypeEnglish': self._HEATING_TYPE_TRANSLATIONS[self.heating_type].english,
            'heatingTypeFrench': self._HEATING_TYPE_TRANSLATIONS[self.heating_type].french,
            'energySourceEnglish': self._ENERGY_SOURCE_TRANSLATIONS[self.energy_source].english,
            'energySourceFrench': self._ENERGY_SOURCE_TRANSLATIONS[self.energy_source].french,
            'equipmentTypeEnglish': self.equipment_type.english,
            'equipmentTypeFrench': self.equipment_type.french,
            'outputSizeKW': self.output_size,
            'outputSizeBtu': self.output_size * self._KWH_TO_BTU,
            'efficiency': self.efficiency,
            'steadyState': self.steady_state,
        }
