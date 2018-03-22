import datetime
import enum
import typing
from dateutil import parser
from energuide import validator
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
    house_id: int
    eval_id: int
    file_id: str
    eval_type: EvaluationType
    entry_date: datetime.date
    creation_date: datetime.datetime
    modification_date: typing.Optional[datetime.datetime]
    year_built: int
    city: str
    region: Region
    forward_sortation_area: str
    ers_rating: typing.Optional[int]
    energy_upgrades: typing.List[upgrade.Upgrade]


class ParsedDwellingDataRow(_ParsedDwellingDataRow):

    _SCHEMA = {
        'EVAL_ID': {'type': 'integer', 'required': True, 'coerce': int},
        'HOUSE_ID': {'type': 'integer', 'required': True, 'coerce': int},
        'EVAL_TYPE': {'type': 'string', 'required': True, 'allowed': [eval_type.value for eval_type in EvaluationType]},
        'ENTRYDATE': {'type': 'date', 'required': True, 'coerce': parser.parse},
        'CREATIONDATE': {'type': 'datetime', 'required': True, 'coerce': parser.parse},
        'YEARBUILT': {'type': 'integer', 'required': True, 'coerce': int},
        'CLIENTCITY': {'type': 'string', 'required': True},
        'forwardSortationArea': {'type': 'string', 'required': True, 'regex': '[A-Z][0-9][A-Z]'},
        'HOUSEREGION': {'type': 'string', 'required': True},
        'BUILDER': {'type': 'string', 'required': True},

        'upgrades': {
            'type': 'list',
            'required': True,
            'schema': {
                'type': 'xml',
                'coerce': 'parse_xml',
            }
        },

        'MODIFICATIONDATE': {'type': 'datetime', 'nullable': True, 'required': True, 'coerce': parser.parse},

        'HEATEDFLOORAREA': {'type': 'float', 'nullable': True, 'coerce': float},
        'TYPEOFHOUSE': {'type': 'string', 'nullable': True},
        'ERSRATING': {'type': 'integer', 'nullable': True, 'coerce': int},
        'UGRERSRATING': {'type': 'integer', 'nullable': True, 'coerce': int},
        'ERSGHG': {'type': 'float', 'nullable': True, 'coerce': float},
        'UGRERSGHG': {'type': 'float', 'nullable': True, 'coerce': float},
        'ERSENERGYINTENSITY': {'type': 'float', 'nullable': True, 'coerce': float},
    }

    @classmethod
    def from_row(cls, row: typing.Dict[str, typing.Any]) -> 'ParsedDwellingDataRow':
        checker = validator.DwellingValidator(cls._SCHEMA, allow_unknown=True)
        if not checker.validate(row):
            error_keys = ', '.join(checker.errors.keys())
            raise InvalidInputDataError(f'Validator failed on keys: {error_keys}')

        parsed = checker.document

        return ParsedDwellingDataRow(
            house_id=parsed['HOUSE_ID'],
            eval_id=parsed['EVAL_ID'],
            file_id=parsed['BUILDER'],
            eval_type=EvaluationType.from_code(parsed['EVAL_TYPE']),
            entry_date=parsed['ENTRYDATE'].date(),
            creation_date=parsed['CREATIONDATE'],
            modification_date=parsed['MODIFICATIONDATE'],
            year_built=parsed['YEARBUILT'],
            city=parsed['CLIENTCITY'],
            region=Region.from_data(parsed['HOUSEREGION']),
            forward_sortation_area=parsed['forwardSortationArea'],

            ers_rating=parsed['ERSRATING'],
            energy_upgrades=[upgrade.Upgrade.from_data(upgrade_node) for upgrade_node in parsed['upgrades']],
        )


class Evaluation:

    def __init__(self, *,
                 file_id: str,
                 evaluation_id: int,
                 evaluation_type: EvaluationType,
                 entry_date: datetime.date,
                 creation_date: datetime.datetime,
                 modification_date: typing.Optional[datetime.datetime],
                 ers_rating: typing.Optional[int],
                 energy_upgrades: typing.List[upgrade.Upgrade],
                ) -> None:
        self._file_id = file_id
        self._evaluation_id = evaluation_id
        self._evaluation_type = evaluation_type
        self._entry_date = entry_date
        self._creation_date = creation_date
        self._modification_date = modification_date
        self._ers_rating = ers_rating
        self._energy_upgrades = energy_upgrades


    @classmethod
    def from_data(cls, data: ParsedDwellingDataRow) -> 'Evaluation':
        return Evaluation(
            file_id=data.file_id,
            evaluation_id=data.eval_id,
            evaluation_type=data.eval_type,
            entry_date=data.entry_date,
            creation_date=data.creation_date,
            modification_date=data.modification_date,
            ers_rating=data.ers_rating,
            energy_upgrades=data.energy_upgrades,
        )

    @property
    def evaluation_type(self) -> EvaluationType:
        return self._evaluation_type

    @property
    def evaluation_id(self) -> int:
        return self._evaluation_id

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
    def modification_date(self) -> typing.Optional[datetime.datetime]:
        return self._modification_date

    @property
    def file_id(self) -> str:
        return self._file_id

    @property
    def energy_upgrades(self) -> typing.List[upgrade.Upgrade]:
        return self._energy_upgrades


    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'fileId': self.file_id,
            'evaluationId': self.evaluation_id,
            'evaluationType': self.evaluation_type.value,
            'entryDate': self.entry_date.isoformat(),
            'creationDate': self.creation_date.isoformat(),
            'modificationDate': self.modification_date.isoformat() if self.modification_date is not None else None,
            'ersRating': self.ers_rating,
            'energyUpgrades': [upgrade.to_dict() for upgrade in self.energy_upgrades],
        }


class Dwelling:

    GROUPING_FIELD = 'HOUSE_ID'

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
        if not data:
            raise InvalidGroupSizeError('Empty groups are invalid')
        evaluations = [Evaluation.from_data(row) for row in data]
        return Dwelling(
            house_id=data[0].house_id,
            year_built=data[0].year_built,
            city=data[0].city,
            region=data[0].region,
            forward_sortation_area=data[0].forward_sortation_area,
            evaluations=evaluations,
        )

    @classmethod
    def from_group(cls, data: typing.List[typing.Dict[str, typing.Any]]) -> 'Dwelling':
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
