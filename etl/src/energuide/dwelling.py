import datetime
import enum
import typing
from dateutil import parser
from energuide import reader
from energuide import validator
from energuide.embedded import ceiling
from energuide.embedded import code
from energuide.embedded import floor
from energuide.embedded import heating
from energuide.embedded import wall
from energuide.embedded import door
from energuide.embedded import window
from energuide.embedded import ventilation
from energuide.embedded import water_heating
from energuide.embedded import heated_floor_area
from energuide.embedded import basement
from energuide.embedded import upgrade
from energuide.exceptions import InvalidGroupSizeError
from energuide.exceptions import InvalidInputDataError


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
            raise InvalidInputDataError(f'Invalid code: {code}')


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
    heating_system: heating.Heating
    foundations: typing.List[basement.Basement]
    ers_rating: typing.Optional[int]
    energy_upgrades: typing.List[upgrade.Upgrade]


def _cast_nullable_string(value: str) -> typing.Optional[int]:
    if value == '':
        return None
    return int(value)


class ParsedDwellingDataRow(_ParsedDwellingDataRow):

    _XML_SCHEMA = {'type': 'xml', 'required': True, 'coerce': 'parse_xml'}
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
        'ERSRATING': {'type': 'integer', 'nullable': True, 'coerce': _cast_nullable_string},

        'ceilings': _XML_LIST_SCHEMA,
        'floors': _XML_LIST_SCHEMA,
        'walls': _XML_LIST_SCHEMA,
        'doors': _XML_LIST_SCHEMA,
        'windows': _XML_LIST_SCHEMA,
        'heatedFloorArea': _XML_SCHEMA,
        'heating_cooling': _XML_SCHEMA,
        'ventilations': _XML_LIST_SCHEMA,
        'waterHeatings': _XML_SCHEMA,
        'basements': _XML_LIST_SCHEMA,
        'crawlspaces': _XML_LIST_SCHEMA,
        'slabs': _XML_LIST_SCHEMA,

        'codes': {'type': 'dict', 'required': True, 'schema': {'wall': _XML_LIST_SCHEMA, 'window': _XML_LIST_SCHEMA}},
        'upgrades': _XML_LIST_SCHEMA,
    }

    @classmethod
    def from_row(cls, row: reader.InputData) -> 'ParsedDwellingDataRow':
        checker = validator.DwellingValidator(cls._SCHEMA, allow_unknown=True, ignore_none_values=True)
        if not checker.validate(row):
            error_keys = ', '.join(checker.errors.keys())
            raise InvalidInputDataError(f'Validator failed on keys: {error_keys}')

        parsed = checker.document
        codes = code.Codes.from_data(parsed['codes'])

        foundations = []
        foundations.extend(
            [basement.Basement.from_data(basement_node) for basement_node in parsed['basements']]
        )
        foundations.extend(
            [basement.Basement.from_data(crawlspace_node) for crawlspace_node in parsed['crawlspaces']]
        )
        foundations.extend(
            [basement.Basement.from_data(slab_node) for slab_node in parsed['slabs']]
        )

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
            heating_system=heating.Heating.from_data(parsed['heating_cooling']),
            foundations=foundations,
            ers_rating=parsed['ERSRATING'],
            energy_upgrades=[upgrade.Upgrade.from_data(upgrade_node) for upgrade_node in parsed['upgrades']],
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
                 foundations: typing.List[basement.Basement],
                 ers_rating: typing.Optional[int],
                 energy_upgrades: typing.List[upgrade.Upgrade],
                 heating_system: heating.Heating,
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
        self._foundations = foundations
        self._ers_rating = ers_rating
        self._energy_upgrades = energy_upgrades
        self._heating_system = heating_system

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
            water_heatings=data.water_heatings,
            foundations=data.foundations,
            ers_rating=data.ers_rating,
            energy_upgrades=data.energy_upgrades,
            heating_system=data.heating_system,
        )

    @property
    def evaluation_type(self) -> EvaluationType:
        return self._evaluation_type

    @property
    def entry_date(self) -> datetime.date:
        return self._entry_date

    @property
    def ers_rating(self) -> typing.Optional[int]:
        return self._ers_rating

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

    @property
    def foundations(self) -> typing.List[basement.Basement]:
        return self._foundations

    @property
    def energy_upgrades(self) -> typing.List[upgrade.Upgrade]:
        return self._energy_upgrades

    @property
    def heating_system(self) -> heating.Heating:
        return self._heating_system

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
            'waterHeatings': [water_heating.to_dict() for water_heating in self.water_heatings],
            'foundations': [foundation.to_dict() for foundation in self.foundations],
            'ersRating': self.ers_rating,
            'energyUgrades': [upgrade.to_dict() for upgrade in self.energy_upgrades],
            'heating': self.heating_system.to_dict(),
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
            raise InvalidGroupSizeError(f'Invalid group size "{len(data)}". Groups must be size 2')

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
