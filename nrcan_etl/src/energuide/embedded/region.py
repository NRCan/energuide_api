import enum
import re
import typing
import unicodedata
import Levenshtein

from energuide import logger


LOGGER = logger.get_logger(__name__)


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
    'YUKON_TERRITORY': 'YUKON',
    'NORTHWEST_TERRITORY': 'NORTHWEST_TERRITORIES',
}

_ALTERNATIVE_CODES = {
    'PEI': 'PE',
    'NWT': 'NT'
}

_MINIMUM_SIMILARITY = 0.6

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

    @classmethod
    def _from_name(cls, name: str) -> typing.Optional['Region']:
        english_region = Region[name] if name in Region.__members__ else None
        if english_region:
            return english_region

        if name in _FRENCH_NAMES:
            return Region[_FRENCH_NAMES[name]]

        if name in _ALTERNATIVE_NAMES:
            return Region[_ALTERNATIVE_NAMES[name]]

        return None


    @classmethod
    def _from_code(cls, code: str) -> typing.Optional['Region']:
        code = code.replace('.', '')
        for region in Region:
            if code == region.value or _ALTERNATIVE_CODES.get(code) == region.value:
                return region

        return None


    @classmethod
    def _from_fuzzy_match(cls, data: str) -> typing.Optional['Region']:
        # Name is prefix of full name
        for region in Region.__members__:
            if region.startswith(data):
                LOGGER.warning(f'PREFIX: Interpreting {data} as {region}')
                return Region[region]

        # Code separated by _
        code = data.replace('_', '')
        region = cls._from_code(code)
        if region:
            return region

        # Levenshtein minimum number of edits to closest region
        ratios = [(Levenshtein.ratio(region, data), region) for region in Region.__members__.keys() - {'UNKNOWN'}]
        ratio, region = max(ratios)

        if ratio > _MINIMUM_SIMILARITY:
            LOGGER.warning(f'SIMILARITY: Interpreting {data} as {region}')
            return Region[region]

        return None

    @classmethod
    def from_data(cls, data: str) -> 'Region':
        if len(data) < 2:
            return Region.UNKNOWN

        snake_name = re.sub('[ -]', '_', data.upper()).strip('.')
        ascii_name = unicodedata.normalize('NFD', snake_name).encode('ascii', 'ignore').decode()
        alphabet_name = re.sub('[^a-zA-Z_]', '', ascii_name)

        output = cls._from_name(alphabet_name)
        if not output:
            output = cls._from_code(alphabet_name)
        if not output:
            output = cls._from_fuzzy_match(alphabet_name)
        if not output:
            output = Region.UNKNOWN

        return output
