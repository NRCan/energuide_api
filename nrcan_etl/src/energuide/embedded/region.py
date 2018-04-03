import enum
import re
import typing
import unicodedata
import Levenshtein

from energuide import logger


LOGGER = logger.get_logger(__name__)


@enum.unique
class Region(enum.Enum):
    BRITISH_COLUMBIA = 'BC'
    ALBERTA = 'AB'
    SASKATCHEWAN = 'SK'
    MANITOBA = 'MB'
    ONTARIO = 'ON'
    QUEBEC = 'QC'
    NEW_BRUNSWICK = 'NB'
    PRINCE_EDWARD_ISLAND = 'PE'
    NOVA_SCOTIA = 'NS'
    NEWFOUNDLAND_AND_LABRADOR = 'NL'
    YUKON = 'YT'
    NORTHWEST_TERRITORIES = 'NT'
    NUNAVUT = 'NU'
    UNKNOWN = '??'

    _FRENCH_NAMES = {
        'ALBERTA': 'ALBERTA',
        'COLOMBIE_BRITANNIQUE': 'BRITISH_COLUMBIA',
        'ILE_DU_PRINCE_EDOUARD': 'PRINCE_EDWARD_ISLAND',
        'MANITOBA': 'MANITOBA',
        'NOUVEAU_BRUNSWICK': 'NEW_BRUNSWICK',
        'NOUVELLE_ECOSSE': 'NOVA_SCOTIA',
        'NUNAVUT': 'NUNAVUT',
        'ONTARIO': 'ONTARIO',
        'QUEBEC': 'QUEBEC',
        'SASKATCHEWAN': 'SASKATCHEWAN',
        'TERRE_NEUVE_ET_LABRADOR': 'NEWFOUNDLAND_AND_LABRADOR',
        'TERRITOIRES_DU_NORD_OUEST': 'NORTHWEST_TERRITORIES',
        'YUKON': 'YUKON'
    }

    _ALTERNATIVE_NAMES = {
        'YUKON_TERRITORY': 'YUKON'
    }

    @classmethod
    def _from_name(cls, name: str) -> typing.Optional['Region']:
        english_region = Region[name] if name in Region.__members__ else None
        if english_name:
            return english_region

        if name in cls._FRENCH_NAMES:
            return Region[cls._FRENCH_NAMES[name]]

        return None


    @classmethod
    def _from_code(cls, code: str) -> typing.Optional['Region']:
        code = code.replace('.', '')
        for region in Region:
            if code == region.value:
                return region

        return None


    @classmethod
    def _from_fuzzy_match(cls, data: str) -> typing.Optional['Region']:
        # Prefix
        for region in Region:
            if region.value.startswith(data):
                LOGGER.warning(f'PREFIX: Interpreting {data} as {region}')
                return region

        ratios = [(Levenshtein.ratio(region, data), region) for region in Region.__members__.keys() - {'UNKNOWN'}]
        ratio, region = max(ratios)

        if ratio > 0.2:
            LOGGER.warning(f'Interpreting {data} as {region}')
            return Region[region]

    @classmethod
    def from_data(cls, data: str) -> 'Region':
        if not data:
            return Region.UNKNOWN

        snake_name = re.sub('[ -]', '_', data.upper()).strip('.')
        ascii_name = unicodedata.normalize('NFD', snake_name).encode('ascii', 'ignore').decode()

        output = cls._from_name(ascii_name)
        if not output:
            output = cls._from_code(ascii_name)
        if not output:
            output = cls._from_fuzzy_match(ascii_name)
        if not output:
            output = Region.UNKNOWN

        return output
