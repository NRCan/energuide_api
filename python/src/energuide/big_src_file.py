from contextlib import contextmanager
import datetime
import enum
import typing
import csv
import json
import os
import sys
import zipfile
import cerberus
import pymongo

from dateutil import parser
from energuide import reader
from energuide import validator
from energuide import element
from energuide import snippets
from energuide import dwelling
from energuide.embedded import ceiling
from energuide.embedded import code
from energuide.embedded import floor
from energuide.embedded import wall
from energuide.embedded import door
from energuide.embedded import window
from energuide.embedded import ventilation
from energuide.embedded import water_heating
from energuide.embedded import heated_floor_area
from energuide.exceptions import InvalidGroupSizeException
from energuide.exceptions import InvalidInputDataException


@enum.unique
class EvaluationType(enum.Enum):
    PRE_RETROFIT = 'D'
    POST_RETROFIT = 'E'

    @classmethod
    def from_code(cls, code: str) -> 'EvaluationType':
        if code == cls.PRE_RETROFIT.value:
            return EvaluationType.PRE_RETROFIT
        elif code == cls.POST_RETROFIT.value:
            return EvaluationType.POST_RETROFIT
        else:
            raise InvalidInputDataException()


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
        snake_name = name.upper().replace(' ', '_')
        return Region[snake_name] if snake_name in Region.__members__ else None

    @classmethod
    def _from_code(cls, code: str) -> typing.Optional['Region']:
        code = code.upper()
        for region in Region:
            if code == region.value:
                return region
        return None

    @classmethod
    def from_data(cls, data: str) -> 'Region':
        output = cls._from_name(data)
        if not output:
            output = cls._from_code(data)
        if not output:
            output = Region.UNKNOWN
        return output


class _ParsedDwellingDataRow(typing.NamedTuple):
    eval_id: int
    eval_type: EvaluationType
    entry_date: datetime.date
    creation_date: datetime.datetime
    modification_date: datetime.datetime
    year_built: int
    city: str
    region: Region
    forward_sortation_area: str
    ceilings: typing.List[ceiling.Ceiling]
    floors: typing.List[floor.Floor]
    walls: typing.List[wall.Wall]
    doors: typing.List[door.Door]
    windows: typing.List[window.Window]
    heated_floor: heated_floor_area.HeatedFloorArea
    water_heatings: typing.List[water_heating.WaterHeating]
    ventilations: typing.List[ventilation.Ventilation]



class ParsedDwellingDataRow(_ParsedDwellingDataRow):

    _XML_SCHEMA = {'type': 'xml', 'coerce': 'parse_xml'}
    _XML_LIST_SCHEMA = {'type': 'list', 'required': True, 'schema': _XML_SCHEMA}

    _SCHEMA = {
        'EVAL_ID': {'type': 'integer', 'required': True, 'coerce': int},
        'EVAL_TYPE': {'type': 'string', 'required': True, 'allowed': [eval_type.value for eval_type in EvaluationType]},
        'ENTRYDATE': {'type': 'date', 'required': True, 'coerce': parser.parse},
        'CREATIONDATE': {'type': 'datetime', 'required': True, 'coerce': parser.parse},
        'MODIFICATIONDATE': {'type': 'datetime', 'required': True, 'coerce': parser.parse},
        'YEARBUILT': {'type': 'integer', 'required': True, 'coerce': int},
        'CLIENTCITY': {'type': 'string', 'required': True},
        'forwardSortationArea': {'type': 'string', 'required': True, 'regex': '[A-Z][0-9][A-Z]'},
        'HOUSEREGION': {'type': 'string', 'required': True},

        'ceilings': _XML_LIST_SCHEMA,
        'floors': _XML_LIST_SCHEMA,
        'walls': _XML_LIST_SCHEMA,
        'doors': _XML_LIST_SCHEMA,
        'windows': _XML_LIST_SCHEMA,
        'heatedFloorArea': _XML_SCHEMA,
        'heating_cooling': {'type': 'xml', 'required': True, 'coerce': 'parse_xml'},
        'ventilations': _XML_LIST_SCHEMA,
        'waterHeatings': _XML_SCHEMA,

        'codes': {'type': 'dict', 'required': True, 'schema': {'wall': _XML_LIST_SCHEMA, 'window': _XML_LIST_SCHEMA}},
    }

    @classmethod
    def from_row(cls, row: reader.InputData) -> 'ParsedDwellingDataRow':
        checker = validator.DwellingValidator(cls._SCHEMA, allow_unknown=True, ignore_none_values=True)
        if not checker.validate(row):
            error_keys = ', '.join(checker.errors.keys())
            raise InvalidInputDataException(f'Validator failed on keys: {error_keys}')

        parsed = checker.document
        codes = code.Codes.from_data(parsed['codes'])

        return ParsedDwellingDataRow(
            eval_id=parsed['EVAL_ID'],
            eval_type=EvaluationType.from_code(parsed['EVAL_TYPE']),
            entry_date=parsed['ENTRYDATE'].date(),
            creation_date=parsed['CREATIONDATE'],
            modification_date=parsed['MODIFICATIONDATE'],
            year_built=parsed['YEARBUILT'],
            city=parsed['CLIENTCITY'],
            region=Region.from_data(parsed['HOUSEREGION']),
            forward_sortation_area=parsed['forwardSortationArea'],
            ceilings=[ceiling.Ceiling.from_data(ceiling_node) for ceiling_node in parsed['ceilings']],
            floors=[floor.Floor.from_data(floor_node) for floor_node in parsed['floors']],
            walls=[wall.Wall.from_data(wall_node, codes.wall) for wall_node in parsed['walls']],
            doors=[door.Door.from_data(door_node) for door_node in parsed['doors']],
            windows=[window.Window.from_data(window_node, codes.window) for window_node in parsed['windows']],
            heated_floor=heated_floor_area.HeatedFloorArea.from_data(parsed['heatedFloorArea']),
            water_heatings=water_heating.WaterHeating.from_data(parsed['waterHeatings']),
            ventilations=[ventilation.Ventilation.from_data(ventilation_node)
                          for ventilation_node in parsed['ventilations']],
        )


class Evaluation:

    def __init__(self, *,
                 evaluation_type: EvaluationType,
                 entry_date: datetime.date,
                 creation_date: datetime.datetime,
                 modification_date: datetime.datetime,
                 ceilings: typing.List[ceiling.Ceiling],
                 floors: typing.List[floor.Floor],
                 walls: typing.List[wall.Wall],
                 doors: typing.List[door.Door],
                 windows: typing.List[window.Window],
                 heated_floor_area: heated_floor_area.HeatedFloorArea,
                 water_heatings: typing.List[water_heating.WaterHeating],
                 ventilations: typing.List[ventilation.Ventilation],
                ) -> None:
        self._evaluation_type = evaluation_type
        self._entry_date = entry_date
        self._creation_date = creation_date
        self._modification_date = modification_date
        self._ceilings = ceilings
        self._floors = floors
        self._walls = walls
        self._doors = doors
        self._windows = windows
        self._heated_floor_area = heated_floor_area
        self._ventilations = ventilations
        self._water_heatings = water_heatings

    @classmethod
    def from_data(cls, data: ParsedDwellingDataRow) -> 'Evaluation':
        return Evaluation(
            evaluation_type=data.eval_type,
            entry_date=data.entry_date,
            creation_date=data.creation_date,
            modification_date=data.modification_date,
            ceilings=data.ceilings,
            floors=data.floors,
            walls=data.walls,
            doors=data.doors,
            windows=data.windows,
            heated_floor_area=data.heated_floor,
            ventilations=data.ventilations,
            water_heatings=data.water_heatings
        )

    @property
    def evaluation_type(self) -> EvaluationType:
        return self._evaluation_type

    @property
    def entry_date(self) -> datetime.date:
        return self._entry_date

    @property
    def creation_date(self) -> datetime.datetime:
        return self._creation_date

    @property
    def modification_date(self) -> datetime.datetime:
        return self._modification_date

    @property
    def ceilings(self) -> typing.List[ceiling.Ceiling]:
        return self._ceilings

    @property
    def floors(self) -> typing.List[floor.Floor]:
        return self._floors

    @property
    def walls(self) -> typing.List[wall.Wall]:
        return self._walls

    @property
    def doors(self) -> typing.List[door.Door]:
        return self._doors

    @property
    def windows(self) -> typing.List[window.Window]:
        return self._windows

    @property
    def heated_floor(self) -> heated_floor_area.HeatedFloorArea:
        return self._heated_floor_area

    @property
    def ventilations(self) -> typing.List[ventilation.Ventilation]:
        return self._ventilations

    @property
    def water_heatings(self) -> typing.List[water_heating.WaterHeating]:
        return self._water_heatings

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'evaluationType': self.evaluation_type.value,
            'entryDate': self.entry_date.isoformat(),
            'creationDate': self.creation_date.isoformat(),
            'modificationDate': self.modification_date.isoformat(),
            'ceilings': [ceiling.to_dict() for ceiling in self.ceilings],
            'floors': [floor.to_dict() for floor in self.floors],
            'walls': [wall.to_dict() for wall in self.walls],
            'doors': [door.to_dict() for door in self.doors],
            'windows': [window.to_dict() for window in self.windows],
            'heatedFloorArea': self.heated_floor.to_dict(),
            'ventilations': [ventilation.to_dict() for ventilation in self.ventilations],
            'waterHeatings': [water_heating.to_dict() for water_heating in self.water_heatings]
        }


class Dwelling:

    GROUPING_FIELD = 'EVAL_ID'

    def __init__(self, *,
                 house_id: int,
                 year_built: int,
                 city: str,
                 region: Region,
                 forward_sortation_area: str,
                 evaluations: typing.List[Evaluation]) -> None:
        self._house_id = house_id
        self._year_built = year_built
        self._city = city
        self._region = region
        self._forward_sortation_area = forward_sortation_area
        self._evaluations = evaluations

    @classmethod
    def _from_parsed_group(cls, data: typing.List[ParsedDwellingDataRow]) -> 'Dwelling':
        if len(data) == 2:
            evaluations = [Evaluation.from_data(row) for row in data]
            return Dwelling(
                house_id=data[0].eval_id,
                year_built=data[0].year_built,
                city=data[0].city,
                region=data[0].region,
                forward_sortation_area=data[0].forward_sortation_area,
                evaluations=evaluations,
            )
        else:
            raise InvalidGroupSizeException()

    @classmethod
    def from_group(cls, data: typing.List[reader.InputData]) -> 'Dwelling':
        parsed_data = [ParsedDwellingDataRow.from_row(row) for row in data]
        return cls._from_parsed_group(parsed_data)

    @property
    def house_id(self) -> int:
        return self._house_id

    @property
    def year_built(self) -> int:
        return self._year_built

    @property
    def city(self) -> str:
        return self._city

    @property
    def region(self) -> Region:
        return self._region

    @property
    def forward_sortation_area(self) -> str:
        return self._forward_sortation_area

    @property
    def evaluations(self) -> typing.List[Evaluation]:
        return self._evaluations

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'houseId': self.house_id,
            'yearBuilt': self.year_built,
            'city': self.city,
            'region': self.region.value,
            'forwardSortationArea': self.forward_sortation_area,
            'evaluations': [evaluation.to_dict() for evaluation in self.evaluations]
        }


class EnvVariables(enum.Enum):
    username = 'ENERGUIDE_USERNAME'
    password = 'ENERGUIDE_PASSWORD'
    host = 'ENERGUIDE_HOST'
    port = 'ENERGUIDE_PORT'
    database = 'ENERGUIDE_DBNAME'
    collection = 'ENERGUIDE_COLLECTION'


class EnvDefaults(enum.Enum):
    username = ''
    password = ''
    host = 'localhost'
    port = 27017
    database = 'energuide'
    collection = 'dwellings'


class DatabaseCoordinates(typing.NamedTuple):
    username: str
    password: str
    host: str
    port: int


def _is_prod() -> bool:
    return bool(os.environ.get('PROD'))


def _build_connection_string(coords: DatabaseCoordinates) -> str:
    username, password, host, port = coords

    if _is_prod():
        connection_string = f'mongodb+srv://{username}:{password}@{host}'
    else:
        prefix = f'{username}:{password}@' if username and password else ''
        connection_string = f'{prefix}{host}:{port}'

    return connection_string


@contextmanager  # type: ignore
def mongo_client(database_coordinates: DatabaseCoordinates) -> typing.Iterable[pymongo.MongoClient]:
    connection_string = _build_connection_string(database_coordinates)
    with pymongo.MongoClient(f'{connection_string}') as client:
        yield client


_DEFAULT_CHUNK_SIZE = 1000


def _chunk_data(data: typing.Iterable[dwelling.Dwelling],
                max_chunk_size: int = _DEFAULT_CHUNK_SIZE
               ) -> typing.Iterator[typing.List[typing.Dict[str, typing.Any]]]:

    chunked_list: typing.List[typing.Dict[str, typing.Any]] = []
    load_size = 0

    for row in data:
        if load_size >= max_chunk_size:
            yield chunked_list
            chunked_list = []
            load_size = 0
        chunked_list.append(row.to_dict())
        load_size += 1

    if chunked_list:
        yield chunked_list


def load(coords: DatabaseCoordinates,
         database_name: str,
         collection_name: str,
         data: typing.Iterable[dwelling.Dwelling]) -> None:
    client: pymongo.MongoClient
    with mongo_client(coords) as client:
        database = client[database_name]
        collection = database[collection_name]

        for data_to_load in _chunk_data(data):
            collection.insert_many(data_to_load)


DROP_FIELDS = ['ENTRYBY',
               'CLIENTNAME',
               'CLIENTADDR',
               'CLIENTPCODE',
               'TELEPHONE',
               'MAIL_ADDR',
               'MAIL_PCODE',
               'TAXNUMBER',
               'RAW_XML',
               'INFO1',
               'INFO2',
               'INFO3',
               'INFO4',
               'INFO5',
               'INFO6',
               'INFO7',
               'INFO8',
               'INFO9',
               'INFO10']

REQUIRED_FIELDS = DROP_FIELDS + [
    'EVAL_ID',
    'EVAL_TYPE',
    'BUILDER',
    'DHWHPCOP',
]

_SCHEMA = {field: {'type': 'string', 'required': True} for field in REQUIRED_FIELDS}


def _validated(data: typing.Iterable[reader.InputData], validator) -> typing.Iterator[reader.InputData]:
    for row in data:
        if not validator.validate(row):
            error_keys = ', '.join(validator.errors.keys())
            raise InvalidInputDataException(f'Validator failed on keys: {error_keys}')
        yield row


def _read_csv(filepath: str) -> typing.Iterator[reader.InputData]:
    csv.field_size_limit(sys.maxsize)
    with open(filepath, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            yield row


def _safe_merge(data: reader.InputData, extra: reader.InputData) -> reader.InputData:
    for key, value in extra.items():
        assert key not in data
        data[key] = value
    return data


def _extract_snippets(data: typing.Iterable[reader.InputData]) -> typing.Iterator[reader.InputData]:
    for row in data:
        row['forwardSortationArea'] = row['CLIENTPCODE'][:3]

        doc = element.Element.from_string(row['RAW_XML'])
        house_node = doc.xpath('House')
        if house_node:
            house_snippets = snippets.snip_house(house_node[0])
            row = _safe_merge(row, house_snippets.to_dict())

        code_node = doc.xpath('Codes')
        if code_node:
            code_snippets = snippets.snip_codes(code_node[0])
            row = _safe_merge(row, code_snippets.to_dict())

        yield row


def _remove_pii_fields(data: typing.Iterable[reader.InputData]) -> typing.Iterator[reader.InputData]:
    for row in data:
        for key in DROP_FIELDS:
            row.pop(key)
        yield row


def extract_data(input_path: str) -> typing.Iterator[reader.InputData]:
    validator = cerberus.Validator(_SCHEMA, allow_unknown=True)
    data = _read_csv(input_path)
    validated_data = _validated(data, validator)
    data_with_snippets = _extract_snippets(validated_data)
    safe_extract = _remove_pii_fields(data_with_snippets)
    return safe_extract


def write_data(data: typing.Iterable[reader.InputData], output_path: str) -> None:
    with zipfile.ZipFile(output_path, mode='w') as output_zip:
        for blob in data:
            blob_id = blob.get('BUILDER')
            if blob_id:
                output_zip.writestr(blob_id, json.dumps(blob))


class _Codes(typing.NamedTuple):
    wall: typing.List[str]
    window: typing.List[str]


class Codes(_Codes):

    def to_dict(self) -> typing.Dict[str, typing.Dict[str, typing.List[str]]]:
        return {
            'codes': {
                'wall': self.wall,
                'window': self.window,
            }
        }


class _HouseSnippet(typing.NamedTuple):
    ceilings: typing.List[str]
    floors: typing.List[str]
    walls: typing.List[str]
    doors: typing.List[str]
    windows: typing.List[str]
    heated_floor_area: typing.Optional[str]
    heating_cooling: typing.Optional[str]
    ventilation: typing.List[str]
    water_heating: typing.Optional[str]
    basements: typing.List[str]
    crawlspaces: typing.List[str]
    slabs: typing.List[str]


class HouseSnippet(_HouseSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'ceilings': self.ceilings,
            'floors': self.floors,
            'walls': self.walls,
            'doors': self.doors,
            'windows': self.windows,
            'heatedFloorArea': self.heated_floor_area,
            'heating_cooling': self.heating_cooling,
            'ventilations': self.ventilation,
            'waterHeatings': self.water_heating,
            'basements': self.basements,
            'crawlspaces': self.crawlspaces,
            'slabs': self.slabs,
        }


def _extract_nodes(node: element.Element, path: str) -> typing.List[element.Element]:
    return node.xpath(path)


def snip_house(house: element.Element) -> HouseSnippet:
    ceilings = _extract_nodes(house, 'Components/Ceiling')
    floors = _extract_nodes(house, 'Components/Floor')
    walls = _extract_nodes(house, 'Components/Wall')
    doors = _extract_nodes(house, 'Components//Components/Door')
    windows = _extract_nodes(house, 'Components//Components/Window')
    heated_floor_area = _extract_nodes(house, 'Specifications/HeatedFloorArea')
    heating_cooling = _extract_nodes(house, 'HeatingCooling')
    heating_cooling_string = heating_cooling[0].to_string() if heating_cooling else None
    ventilation = _extract_nodes(house, 'Ventilation/WholeHouseVentilatorList/Hrv')
    ventilation_strings = [hrv.to_string() for hrv in ventilation]

    water_heating = _extract_nodes(house, 'Components/HotWater')
    water_heating_string = water_heating[0].to_string() if water_heating else None

    basements = _extract_nodes(house, 'Components/Basement')
    crawlspaces = _extract_nodes(house, 'Components/Crawlspace')
    slabs = _extract_nodes(house, 'Components/Slab')

    return HouseSnippet(
        ceilings=[node.to_string() for node in ceilings],
        floors=[node.to_string() for node in floors],
        walls=[node.to_string() for node in walls],
        doors=[node.to_string() for node in doors],
        windows=[node.to_string() for node in windows],
        heated_floor_area=heated_floor_area[0].to_string() if heated_floor_area else None,
        heating_cooling=heating_cooling_string,
        ventilation=ventilation_strings,
        water_heating=water_heating_string,
        basements=[node.to_string() for node in basements],
        crawlspaces=[node.to_string() for node in crawlspaces],
        slabs=[node.to_string() for node in slabs],
    )


def snip_codes(codes: element.Element) -> Codes:
    wall_codes = codes.xpath('Wall/*/Code')
    window_codes = codes.xpath('Window/*/Code')

    return Codes(
        wall=[node.to_string() for node in wall_codes],
        window=[node.to_string() for node in window_codes],
    )
